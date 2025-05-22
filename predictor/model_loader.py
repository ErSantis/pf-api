import torch
import torch.nn as nn
from torchvision import models

class SkinDiseaseModel:
    def __init__(self, model_path, num_classes):
        self.model = models.resnet50(pretrained=False)
        self.model.fc = nn.Sequential(
            nn.Linear(2048, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()
        
    def predict(self, image_tensor):
        with torch.no_grad():
            output = self.model(image_tensor.unsqueeze(0))
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            top_prob, top_class = torch.max(probabilities, 0)
            
            class_idx = top_class.item()
            confidence = top_prob.item() * 100
            
            return {
                "class_id": class_idx,
                "confidence": round(confidence, 2)
            }
