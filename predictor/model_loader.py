import torch
import torch.nn as nn
from torchvision import models

# Definición de enfermedades de la piel y recomendaciones
SKIN_DISEASES = [
  {
    "condition": "Acné",
    "description":
      "El acné es una enfermedad inflamatoria de la piel que se presenta con espinillas, puntos negros y granos, comúnmente en la cara, pecho y espalda.",
    "recommendations": [
      "Lavar el rostro dos veces al día con un limpiador suave",
      "Evitar apretar o reventar los granos",
      "Usar productos no comedogénicos",
      "Consultar con un dermatólogo si el acné es severo o persistente",
    ],
  },
  {
    "condition": "Dermatitis Atópica",
    "description":
      "La dermatitis atópica es una afección crónica que provoca enrojecimiento, picazón intensa y sequedad en la piel.",
    "recommendations": [
      "Hidratar la piel con cremas emolientes varias veces al día",
      "Evitar el uso de productos irritantes o perfumados",
      "Mantener las uñas cortas para reducir el daño al rascarse",
      "Consultar con un dermatólogo sobre posibles tratamientos con corticoides o inmunomoduladores",
    ],
  },
  {
    "condition": "Tumor Benigno",
    "description":
      "Un tumor benigno de la piel es un crecimiento no canceroso que puede aparecer como un lunar, quiste o lipoma.",
    "recommendations": [
      "Monitorear cualquier cambio en tamaño, forma o color",
      "Evitar la manipulación de los tumores",
      "Consultar al dermatólogo si hay crecimiento rápido o molestias",
      "Realizar revisiones periódicas para descartar malignidad",
    ],
  },
  {
    "condition": "Cáncer de Piel",
    "description":
      "El cáncer de piel es una proliferación maligna de células cutáneas, puede presentarse como lesiones nuevas, cambios en lunares o heridas que no cicatrizan.",
    "recommendations": [
      "Evitar la exposición solar prolongada y usar protector solar diariamente",
      "Consultar de inmediato si hay cambios sospechosos en la piel",
      "Revisarse periódicamente los lunares y manchas",
      "Seguir tratamiento médico especializado según el tipo de cáncer",
    ],
  },
  {
    "condition": "Dermatitis por Contacto",
    "description":
      "La dermatitis por contacto es una inflamación de la piel causada por el contacto con sustancias irritantes o alérgenas.",
    "recommendations": [
      "Identificar y evitar el contacto con el agente causante",
      "Aplicar cremas con corticoides si es necesario",
      "Usar guantes si se manipulan productos químicos",
      "Hidratar la piel para ayudar a su recuperación",
    ],
  },
  {
    "condition": "Erupción Medicamentosa",
    "description":
      "El exantema por medicamentos es una reacción adversa de la piel a ciertos fármacos, que puede incluir erupciones, enrojecimiento y picazón.",
    "recommendations": [
      "Suspender el medicamento causante bajo supervisión médica",
      "Consultar de inmediato con un médico ante cualquier reacción cutánea grave",
      "Evitar la automedicación",
      "Usar antihistamínicos para aliviar la picazón si es indicado",
    ],
  },
  {
    "condition": "Eccema",
    "description":
      "El eccema es una afección inflamatoria de la piel que provoca picazón, enrojecimiento y descamación.",
    "recommendations": [
      "Hidratar la piel frecuentemente con emolientes",
      "Evitar el uso de jabones fuertes o perfumados",
      "Reducir el estrés, que puede empeorar los síntomas",
      "Consultar con un dermatólogo para tratamiento con corticoides tópicos o fototerapia",
    ],
  },
  {
    "condition": "Infección Fúngica",
    "description":
      "Las infecciones fúngicas de la piel son causadas por hongos y pueden producir enrojecimiento, descamación, picazón y mal olor.",
    "recommendations": [
      "Mantener la piel limpia y seca",
      "Evitar compartir objetos personales como toallas o calzado",
      "Usar antifúngicos tópicos o sistémicos según prescripción médica",
      "Lavar la ropa con agua caliente para eliminar esporas",
    ],
  },
  {
    "condition": "Melanoma",
    "description":
      "El melanoma es un tipo agresivo de cáncer de piel que se origina en los melanocitos y puede diseminarse rápidamente.",
    "recommendations": [
      "Consultar de inmediato si aparece un lunar nuevo o uno existente cambia de forma, color o tamaño",
      "Evitar la exposición solar intensa y usar protector solar de amplio espectro",
      "Realizar controles dermatológicos periódicos",
      "Seguir el tratamiento oncológico indicado sin demoras",
    ],
  },
  {
    "condition": "Hongos en las Uñas",
    "description":
      "La onicomicosis es una infección fúngica que afecta las uñas, haciéndolas gruesas, frágiles y decoloradas.",
    "recommendations": [
      "Mantener las uñas secas y cortas",
      "Evitar caminar descalzo en lugares públicos como duchas o piscinas",
      "Usar tratamientos antifúngicos prescritos (tópicos u orales)",
      "Desinfectar herramientas para el cuidado de uñas",
    ],
  },
  {
    "condition": "Alteraciones de la Pigmentación",
    "description":
      "Las alteraciones de la pigmentación de la piel pueden incluir manchas oscuras (hiperpigmentación) o claras (hipopigmentación) por diversas causas.",
    "recommendations": [
      "Usar protector solar diariamente para prevenir empeoramiento",
      "Evitar el rascado o manipulación de las lesiones",
      "Consultar con un dermatólogo para tratamientos despigmentantes o láser",
      "Tener paciencia, ya que los tratamientos pueden tardar en mostrar efectos",
    ],
  },
  {
    "condition": "Psoriasis",
    "description":
      "La psoriasis es una enfermedad autoinmune crónica que causa placas rojas con escamas plateadas en la piel.",
    "recommendations": [
      "Hidratar la piel frecuentemente",
      "Evitar factores desencadenantes como el estrés y el alcohol",
      "Consultar con un dermatólogo para tratamiento con tópicos, fototerapia o medicamentos sistémicos",
      "Evitar rascarse para no agravar las lesiones",
    ],
  },
  {
    "condition": "Sarna",
    "description":
      "La sarna es una infestación de la piel causada por un ácaro que provoca intensa picazón, especialmente durante la noche.",
    "recommendations": [
      "Aplicar tratamientos antiparasitarios tópicos según indicación médica",
      "Lavar toda la ropa y sábanas con agua caliente",
      "Evitar el contacto cercano con otras personas hasta tratar la infestación",
      "Tratar a todos los convivientes simultáneamente",
    ],
  },
  {
    "condition": "Enfermedades de Transmisión Sexual",
    "description":
      "Las enfermedades de transmisión sexual pueden presentar manifestaciones cutáneas como úlceras, erupciones o verrugas en los genitales o en otras partes del cuerpo.",
    "recommendations": [
      "Consultar con un profesional de salud para diagnóstico y tratamiento adecuado",
      "Evitar relaciones sexuales hasta recibir tratamiento completo",
      "Usar preservativo en todas las relaciones sexuales",
      "Informar a las parejas sexuales para que también reciban atención",
    ],
  },
  {
    "condition": "Verrugas",
    "description":
      "Las verrugas son crecimientos cutáneos causados por el virus del papiloma humano (VPH), pueden aparecer en manos, pies, cara o genitales.",
    "recommendations": [
      "Evitar tocar o rascarse las verrugas",
      "Consultar con un dermatólogo sobre opciones como crioterapia o tratamientos tópicos",
      "No compartir objetos personales como toallas o cuchillas",
      "Mantener la piel limpia y seca",
    ],
  },
]


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
        
        # Usar las primeras num_classes enfermedades de la lista
        self.diseases = SKIN_DISEASES[:num_classes]

    def predict(self, image_tensor):
        with torch.no_grad():
            output = self.model(image_tensor.unsqueeze(0))
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            top_prob, top_class = torch.max(probabilities, 0)
            
            class_idx = top_class.item()
            confidence = top_prob.item() * 100
            
            # Obtener el nombre de la enfermedad y las recomendaciones
            if class_idx < len(self.diseases):
                disease_info = self.diseases[class_idx]
                disease_name = disease_info["condition"]
                disease_description = disease_info["description"]
                recommendations = disease_info["recommendations"]
            else:
                disease_name = f"Clase {class_idx}"
                disease_description = "No hay descripción disponible."
                recommendations = ["Consultar a un dermatólogo para un diagnóstico preciso."]
            
            return {
                "class_id": class_idx,
                "disease_name": disease_name,
                "description": disease_description,
                "confidence": round(confidence, 2),
                "recommendations": recommendations
            }
