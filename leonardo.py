import requests
import instance
import config

class LeonardoAI:
    def __init__(self):
        self.admin_id = config.admin_id
        self.bot = instance.bot
        self.url = "https://cloud.leonardo.ai/api/rest/v1"
        self.url_gen =f"{self.url}/generations"
        self.url_element = f"{self.url}/elements"
        self.url_model = f"{self.url}/platformModels"
        self.token = config.leonardo_token
        self.leonardo_diffusion_XL = "1e60896f-3c26-4296-8ecc-53e2afecc132"
        self.PhotoReal_model = "b75a5b32-ca22-4b1d-bb0a-883c26783c71"
        self.test_model = 'b700cad2-0e4b-422a-a794-781f20d1e89e'
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.token}"
        }
        
    def generation(self, prompt, alchemy=False, highContrast=False, highResolution=True, photoReal=False, elements=None):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}"
        }
        payload = {
            "height": 512,
            "prompt": prompt,
            "width": 512,
            "num_images": 1,
            "alchemy": alchemy,
            "guidance_scale": 7,
            "highContrast": highContrast,
            "highResolution": highResolution,
            "num_images": 1,
            "photoReal": photoReal,
            "presetStyle": "CINEMATIC",
            "photoRealStrength": 0.5,
            "negative_prompt": "too many feet, too many fingers, long neck, 2 heads, duplicate, abstract, disfigured, deformed, figure, framed, disfigured, bad art, deformed, poorly drawn, extra limbs, weird colors, 2 heads, elongated body, cropped image, out of frame, draft, deformed hands, twisted fingers, double image, malformed hands, multiple heads, extra limb, ugly, poorly drawn hands, missing limb, cut-off, over satured, grain, lowères, bad anatomy, poorly drawn face, mutation, mutated, floating limbs, disconnected limbs, out of focus, long body, disgusting, extra fingers, groos proportions, missing arms, mutated hands, cloned face, missing legs"
        }
        if alchemy:
            payload["presetStyle"] = "CINEMATIC"
        else:
            payload["presetStyle"] = "LEONARDO"
            
        if photoReal:
            payload["modelId"] = self.PhotoReal_model
        else:
            payload["modelId"] = self.leonardo_diffusion_XL

        if elements is not None:
            elements = {key: float(value) for key, value in elements.items()}
            payload["elements"] = [{"akUUID": id, "weight": weight} for id, weight in elements.items()]

        # if elements:
        #     payload["elements"] = []
        #     for element in elements:
        #         element_id, element_weight = element
        #         payload["elements"].append({"akUUID": element_id, "weight": element_weight or 0.5})

        response = requests.post(self.url_gen, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: {response.status_code} 😢")
        
    
    async def get_image(self, generation_id, prompt, photo_real):
        prompt = prompt.replace(" ", "_").replace(",", "")
        prompt = prompt[:54]
        if photo_real:
            model_id = self.PhotoReal_model
        else:
            model_id = self.leonardo_diffusion_XL
        url =f"https://cdn.leonardo.ai/users/8d44b3af-399e-4af0-a041-483d44f48cac/generations/{generation_id}/Default_{prompt}_0.jpg"
        # url = f"{self.url_gen}/{generation_id}"
        # url = "https://cloud.leonardo.ai/api/rest/v1/generations/user/userId?offset=0&limit=10"

        # response = requests.get(url, headers=self.headers)
        # result = response.json()
        return url
 
    def get_element(self):
        response = requests.get(self.url_element, headers=self.headers)
        result = response.json()
        return result
    
    def get_model(self):
        response = requests.get(self.url_model, headers=self.headers)
        result = response.json()
        return result


