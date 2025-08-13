from ultralytics import YOLO

def main():
    # 1. 数据集配置
    data_yaml = r"F:\yolov5\dataset\dataset.yml"  # 使用原始字符串避免转义

    # 2. 加载模型并训练
    model = YOLO("yolov5s.pt")
    model.train(
        data=data_yaml,
        epochs=100,
        # 色彩增强 (HSV空间)
        hsv_h=0.015,  # 色调变化 (±1.5%)
        hsv_s=0.7,    # 饱和度变化 (±70%)
        hsv_v=0.4,    # 明度变化 (±40%)
        # 几何增强
        degrees=10,    # 旋转角度 (±10度)
        translate=0.1, # 平移 (±10%)
        scale=0.5,     # 缩放 (50%-150%)
        fliplr=0.5,    # 50%概率水平翻转
        mosaic=1.0,    # 100%启用马赛克增强(4图合成)
        # 高级增强
        mixup=0.1,     # 10%概率使用MixUp
        copy_paste=0.1 # 10%概率复制粘贴物体(需分割任务)
    )

if __name__ == '__main__':
    main()  # Windows 必须在此保护下执行多进程
    
    
    

