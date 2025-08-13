from ultralytics import YOLO

model = YOLO(r"F:\yolov5\runs\detect\train4\weights\best.pt")  # 你的训练模型

model.export(format='onnx', opset=11, imgsz=640, simplify=True, dynamic=False)