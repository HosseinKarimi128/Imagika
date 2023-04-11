# import os
# import uuid
# from asgiref.sync import sync_to_async
# from davinchi.schemas import *

# import jax
# import numpy as np
# import jax.numpy as jnp
# from flax.jax_utils import replicate
# from flax.training.common_utils import shard
# import requests
# from io import BytesIO
# from PIL import Image
# from diffusers import FlaxStableDiffusionImg2ImgPipeline, StableDiffusionPipeline

# #TODO read all constant from config table
# #SERVICE ===
# async def on_generate_image(request:PostFromCelestial) -> PostForCelestial:
#     image_file = os.path.join('images', request.image+'.png')
#     diffusers_in = DiffusersIn(
#         seed= 0,
#         model_address= 'CompVis/stable-diffusion-v1-4' ,
#         strength = 0.75,
#         prompt= request.prompt,
#         helper_prompt= ' ,artstation',
#         n_prompt= request.n_prompt,
#         image= image_file
#     )
#     deffusers_out = await stable_diffusion_hands(inputs = diffusers_in)
#     return await PostForCelestial(images = await dict(enumerate(deffusers_out.images)))

# # AXILARY
# # @sync_to_async
# def stable_diffusion_hands(inputs:DiffusersIn) -> DiffusersOut:
#     '''
#     def create_key(seed=inputs.seed):
#         return jax.random.PRNGKey(seed)
#     rng = create_key(0)
#     with open(inputs.image, 'rb') as f:
#         img_data = f.read()
#     # url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"
#     # response = requests.get(url)
#     init_img = Image.open(BytesIO(img_data)).convert("RGB")
#     init_img = init_img.resize((768, 512))

#     prompts = inputs.prompt + inputs.helper_prompt
#     neg_prompt = inputs.n_prompt
#     pipeline, params = FlaxStableDiffusionImg2ImgPipeline.from_pretrained(
#         inputs.model_address, revision="flax",
#         dtype=jnp.bfloat16,
#     )

#     num_samples = jax.device_count()
#     rng = jax.random.split(rng, jax.device_count())
#     prompt_ids, processed_image = pipeline.prepare_inputs(prompt=[prompts]*num_samples, image = [init_img]*num_samples)
#     p_params = replicate(params)
#     prompt_ids = shard(prompt_ids)
#     neg_prompt_ids = neg_prompt
#     processed_image = shard(processed_image)
#     output = pipeline(
#         prompt_ids=prompt_ids, 
#         # neg_prompt_ids=neg_prompt_ids,
#         image=processed_image, 
#         params=p_params, 
#         prng_seed=rng, 
#         strength=0.75, 
#         num_inference_steps=50, 
#         jit=True, 
#         height=512,
#         width=768).images
#         output_images = pipeline.numpy_to_pil(np.asarray(output.reshape((num_samples,) + output.shape[-3:])))

#     '''
#     from diffusers import StableDiffusionPipeline
#     # from PIL import Image

#     model_id = "runwayml/stable-diffusion-v1-5"
#     pipe = StableDiffusionPipeline.from_pretrained(model_id)
#     pipe = pipe.to("cuda")

#     prompt = "a photo of an astronaut riding a horse on mars"
#     output = pipe(prompt).images
#     image_names = []
#     for i,image in enumerate(output):
#         image_names[i] = str(uuid.uuid4())
#         image_file = os.path.join('generated_images', image_names[i])
#         with open(image_file, 'w') as f:
#             f.write(image)
#     return DiffusersOut(images = image_names)