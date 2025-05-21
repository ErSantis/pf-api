from torchvision import transforms

val_test_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.4383, 0.3343, 0.3074],
                         std=[0.2298, 0.1865, 0.1763])
])
