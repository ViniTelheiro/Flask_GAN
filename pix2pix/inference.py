from .model import Pix2PixGenerator, desnormalize
import numpy as np
import torchvision.transforms as transforms
import torch
import cv2

def transformer(img):
    transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((256,256)),
            transforms.Normalize(.5,.5)
    ])

    return transform(img)

def read_rgb(img_path:str):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    return img


def generate_img(img_path:str, file_name:str):
    input_img = read_rgb(img_path)
    input_img = transformer(input_img)

    generator = Pix2PixGenerator()
    generator.load_state_dict(torch.load('./pix2pix/log/generator.pth')['model_state_dict'])
    
    generator.eval()
    generated_img = generator(input_img.unsqueeze(0))
    generated_img = desnormalize(generated_img).squeeze(0)
    generated_img = cv2.cvtColor(generated_img, cv2.COLOR_RGB2BGR)
    
    cv2.imwrite(f"./static/generated/{file_name}", generated_img)
    
    return generated_img
    