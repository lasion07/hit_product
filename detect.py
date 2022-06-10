import cv2, os, mmpose, argparse, torch, torchvision, mmdet, glob
from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                        vis_pose_result, process_mmdet_results)
from mmdet.apis import inference_detector, init_detector


parser = argparse.ArgumentParser(description="MMpose")
parser.add_argument('--source', type=str, help="input video or image or camera")
parser.add_argument('--device', type=str, help="cpu or cuda:0")
parser.add_argument('--merge', type=bool, help="Image to Video")
args = parser.parse_args()





pose_config = 'mmpose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/2xrsn50_coco_256x192.py'
pose_checkpoint = 'https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth'
det_config = 'mmpose/demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py'
det_checkpoint = 'https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth'
source = args.source
dc = args.device
merge = args.merge
if dc == None:
    dc = "cpu"
if source != None:
    source = source.replace('\\', '/')
    source = source.split('/')
pose_model = init_pose_model(pose_config, pose_checkpoint, device=dc)
det_model = init_detector(det_config, det_checkpoint, device=dc)

def detect_img(img):
    mmdet_results = inference_detector(det_model, img)
    person_results = process_mmdet_results(mmdet_results, cat_id=1)
    pose_results, _ = inference_top_down_pose_model(
        pose_model,
        img,
        person_results,
        bbox_thr=0.3,
        format='xyxy',
        dataset=pose_model.cfg.data.test.type
    )
    vis_results = vis_pose_result(
        pose_model,
        img,
        pose_results,
        dataset = pose_model.cfg.data.test.type,
        show = False
    )
    vis_results = cv2.resize(vis_results, dsize= None, fx= 0.5, fy= 0.5)
    return vis_results



def merge_video(source: str, log_file: str, output="run/video/project.mp4"):
    """
        source: a/b/
            - jpg
        num_frame: number of frame
    """
    num_frame = 0
    with open(log_file, mode = 'r') as f:
        num_frame = int(f.readline())
    w = None
    h = None
    fps = 30.0
    image_array = []
    for _ in range(num_frame):
        img = cv2.imread(source + str(_) + ".jpg")
        h, w, r = img.shape
        image_array.append(img)
    out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    for frame in image_array:
        out.write(frame)
    out.release()



N = 0
if merge != None:
    merge_video("run/image/", "run/log.txt")
else:
    if source[-1] == 'image':
        for filename in glob.glob("data/image/*.jpg"):
            img = cv2.imread(filename)
            img = detect_img(img)
            cv2.imwrite("run/image/" + str(N) + ".jpg", img)
            N+=1
    elif source[-1].split('.')[-1] == 'jpg':
        source = '/'.join(source)
        img = cv2.imread(source)
        img = detect_img(img)
        source = '/'.join(source.split('/')[1:])
        print(source)
        cv2.imwrite("run/" + source, img)