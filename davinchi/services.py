import os
import uuid
from asgiref.sync import sync_to_async
from davinchi.schemas import *

import jax
import numpy as np
import jax.numpy as jnp
from flax.jax_utils import replicate
from flax.training.common_utils import shard
import requests
from io import BytesIO
from PIL import Image
from diffusers import FlaxStableDiffusionImg2ImgPipeline

#TODO read all constant from config table
#SERVICE ===
async def on_generate_image(request:PostFromCelestial) -> PostForSelestial:
    image_file = os.path.join('images', request.image+'.png')
    with open(image_file, 'r') as i:
        uploaded_image = i.read()
    diffusers_in = DiffusersIn(
        seed= 0,
        model_address= 'CompVis/stable-diffusion-v1-4' ,
        strength = 0.75,
        prompt= request.prompt,
        helper_prompt= ' ,artstation',
        n_prompt= request.n_prompt,
        image= uploaded_image
    )
    deffusers_out = await stable_diffusion_hands(inputs = diffusers_in)
    return await PostForSelestial(images = await dict(enumerate(deffusers_out.images)))

# AXILARY
# @sync_to_async
def stable_diffusion_hands(inputs:DiffusersIn) -> DiffusersOut:
    def create_key(seed=inputs.seed):
        return jax.random.PRNGKey(seed)
    rng = create_key(0)
    # url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"
    # response = requests.get(url)
    init_img = Image.open(BytesIO(inputs.image)).convert("RGB")
    init_img = init_img.resize((768, 512))

    prompts = inputs.prompt + inputs.helper_prompt
    neg_prompt = inputs.n_prompt
    pipeline, params = FlaxStableDiffusionImg2ImgPipeline.from_pretrained(
        inputs.model_address, revision="flax",
        dtype=jnp.bfloat16,
    )

    num_samples = jax.device_count()
    rng = jax.random.split(rng, jax.device_count())
    prompt_ids, processed_image = pipeline.prepare_inputs(prompt=[prompts]*num_samples, image = [init_img]*num_samples)
    p_params = replicate(params)
    prompt_ids = shard(prompt_ids)
    neg_prompt_ids = shard(neg_prompt)
    processed_image = shard(processed_image)
    output = pipeline(
        prompt_ids=prompt_ids, 
        neg_prompt_ids=neg_prompt_ids,
        image=processed_image, 
        params=p_params, 
        prng_seed=rng, 
        strength=0.75, 
        num_inference_steps=50, 
        jit=True, 
        height=512,
        width=768).images
    output_images = pipeline.numpy_to_pil(np.asarray(output.reshape((num_samples,) + output.shape[-3:])))
    image_names = []
    for i,image in enumerate(output_images):
        image_names[i] = str(uuid.uuid4())
        image_file = os.path.join('generated_images', image_names[i])
        with open(image_file, 'w') as f:
            f.write(image)
    return DiffusersOut(images = output_images)