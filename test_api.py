# test_api.py
import requests
import os

def test_prediction_api():
    # Url del endpoint
    url = "http://localhost:8000/api/predict/"
    
    # Verificamos si existe el archivo de prueba
    image_path = "test3.jpg"  # Utilizamos la imagen que ya existe en el directorio
    
    if not os.path.exists(image_path):
        print(f"Error: No se encontró la imagen de prueba '{image_path}'")
        return
    
    # Preparamos el archivo para enviar
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        
        try:
            # Hacemos la petición POST
            print("Enviando petición al servidor...")
            response = requests.post(url, files=files)
            
            # Mostramos la respuesta
            print(f"Código de estado: {response.status_code}")
            if response.status_code == 200:
                print("Respuesta exitosa!")
                print(f"Predicción: {response.json()}")
            else:
                print(f"Error en la respuesta: {response.text}")
        
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Django esté corriendo.")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    test_prediction_api()
