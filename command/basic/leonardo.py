import requests
from . import instance
from . import config

class LeonardoAI:
    def __init__(self):
        self.admin_id = config.admin_id
        self.bot = instance.bot
        self.url = "https://cloud.leonardo.ai/api/rest/v1"
        self.url_gen =f"{self.url}/generations"
        self.url_element = f"{self.url}/elements"
        self.url_model = f"{self.url}/platformModels"
        self.token = config.leonardo_token
        self.test_model = 'b700cad2-0e4b-422a-a794-781f20d1e89e'
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.token}"
        }
        
    def generation(self, prompt, modelId, alchemy=False, highContrast=False, highResolution=True, photoReal=False, elements=None, presetStyle='general', size='512x512'):
        width, height = map(int, size.split('x'))
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}"
        }
        payload = {
            "height": height,
            "prompt": prompt,
            "width": width,
            "num_images": 1,
            "alchemy": alchemy,
            "guidance_scale": 7,
            "highContrast": highContrast,
            "highResolution": highResolution,
            "modelId": modelId,
            "num_images": 1,
            "photoReal": photoReal,
            "presetStyle": presetStyle,
            "photoRealStrength": 0.5,
            "negative_prompt": "too many feet, too many fingers, long neck, 2 heads, duplicate, abstract, disfigured, deformed, figure, framed, disfigured, bad art, deformed, poorly drawn, extra limbs, weird colors, 2 heads, elongated body, cropped image, out of frame, draft, deformed hands, twisted fingers, double image, malformed hands, multiple heads, extra limb, ugly, poorly drawn hands, missing limb, cut-off, over satured, grain, lowères, bad anatomy, poorly drawn face, mutation, mutated, floating limbs, disconnected limbs, out of focus, long body, disgusting, extra fingers, groos proportions, missing arms, mutated hands, cloned face, missing legs"
        }

        if elements is not None:
            elements = {key: float(value['weight']) if isinstance(value, dict) and 'weight' in value else float(value) for key, value in elements.items()}

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
            result = response.json()
            error = result.get('error', None)
            print(f"Error: {response.status_code} 😢")
            raise Exception(error)

    
    def get_image(self, generation_id, prompt=None):
        url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
        response = requests.get(url, headers=self.headers)
        result = response.json()
        result = result.get("generations_by_pk")
        result = result.get("generated_images")
        result = result[0] if result else None
        result = result.get("url") if result else None
        return result
 
    def get_element(self):
        response = requests.get(self.url_element, headers=self.headers)
        result = response.json()
        return result
    
    def get_model(self):
        response = requests.get(self.url_model, headers=self.headers)
        result = response.json()
        return result


