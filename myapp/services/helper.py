import cv2
import numpy as np
import torch

# Load the model
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='dna_train0905.pt')  # Update the path to your model file
model_names = list(model.names.values())


def draw_results(img, results, model_names):
    halo_counts = {name: 0 for name in model_names}
    halo_counts['total'] = 0

    # Extract data from results
    labels = results.xyxy[0][:, -1].cpu().numpy()  # Class IDs, moved to CPU
    boxes = results.xyxy[0][:, :4].cpu().numpy()  # Bounding boxes, moved to CPU
    confidences = results.xyxy[0][:, 4].cpu().numpy()  # Confidences, moved to CPU

    # Convert img from RGB to BGR (for OpenCV rendering)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Draw bounding boxes and labels
    for (x1, y1, x2, y2), label, conf in zip(boxes, labels, confidences):
        class_name = model_names[int(label)]
        color = (int(torch.randint(0, 255, (1,)).item()),
                 int(torch.randint(0, 255, (1,)).item()),
                 int(torch.randint(0, 255, (1,)).item()))  # Random color for each class
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        label_text = f'{class_name} {conf:.2f}'
        cv2.putText(img, label_text, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Update counts
        halo_counts[class_name] += 1
        halo_counts['total'] += 1

    return img, halo_counts


def draw_boundaries(img):
    results = model(img)
    output_img, halo_counts = draw_results(img, results, model_names)
    return output_img, halo_counts
