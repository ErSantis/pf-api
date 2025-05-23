from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
from .serializers import ImageUploadSerializer
from .transform import val_test_transforms
from .model_loader import SkinDiseaseModel
import os

# Inicializa el modelo una vez
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './model/best_model.pth')
model = SkinDiseaseModel(model_path, num_classes=15)  # Actualizado para coincidir con el modelo guardado

class PredictView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = Image.open(serializer.validated_data['image']).convert('RGB')
            image_tensor = val_test_transforms(image)
            prediction = model.predict(image_tensor)
            
            # Devolvemos el nombre de la enfermedad, la confianza y las recomendaciones
            return Response({
                'enfermedad': prediction['disease_name'],
                'confianza': prediction['confidence'],
                'descripcion': prediction['description'],
                'recomendaciones': prediction['recommendations'],
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
