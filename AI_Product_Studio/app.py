import streamlit as st
import torch
from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel, DDIMScheduler
from PIL import Image
import cv2
import numpy as np
from rembg import remove
import gc

# --- CẤU HÌNH ---
LORA_PATH = "/content/drive/MyDrive/Loras/prostudio/output/prostudio-10.safetensors"
TRIGGER_WORD = "prostudio style"

# Dùng Model DreamShaper 8 (Mới hơn, đẹp hơn, hỗ trợ safetensors chuẩn)
BASE_MODEL = "Lykon/dreamshaper-8-inpainting"

@st.cache_resource
def load_models():
    # 1. Load ControlNet
    st.write("⏳ Đang tải ControlNet (1/3)...")
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_canny",
        torch_dtype=torch.float16,
        use_safetensors=True
    )

    # 2. Load Model Chính (Dùng DreamShaper)
    st.write(f"⏳ Đang tải Model chính: {BASE_MODEL} (2/3)...")
    pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
        BASE_MODEL,
        controlnet=controlnet,
        torch_dtype=torch.float16,
        use_safetensors=True,
        safety_checker=None,
        low_cpu_mem_usage=True # <--- QUAN TRỌNG: Chống tràn RAM
    )

    # 3. Load LoRA
    st.write("⏳ Đang nạp LoRA (3/3)...")
    try:
        pipe.load_lora_weights(LORA_PATH)
        pipe.fuse_lora()
        st.write("✅ Đã nạp LoRA thành công!")
    except Exception as e:
        st.warning(f"⚠️ Không tìm thấy LoRA (Sẽ chạy model gốc). Lỗi: {e}")

    # 4. Đẩy sang GPU
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    pipe.to("cuda")

    return pipe

def process_image(input_image, prompt, negative_prompt, pipe):
    w, h = 512, 512

    # Xử lý ảnh đầu vào
    no_bg = remove(input_image)
    mask = Image.fromarray(255 - np.array(no_bg.split()[-1]))

    img_array = np.array(input_image.resize((w, h)))
    canny = cv2.Canny(img_array, 100, 200)
    canny = np.concatenate([canny[:, :, None]] * 3, axis=2)
    canny_img = Image.fromarray(canny)

    # Dọn dẹp bộ nhớ trước khi vẽ
    torch.cuda.empty_cache()
    gc.collect()

    result = pipe(
        prompt=f"{TRIGGER_WORD}, {prompt}, best quality, 8k, masterpiece, ultra realistic",
        negative_prompt=negative_prompt,
        image=input_image.resize((w, h)),
        mask_image=mask.resize((w, h)),
        control_image=canny_img.resize((w, h)),
        num_inference_steps=30,
        guidance_scale=7.5,
        strength=1.0
    ).images[0]

    return result

# --- GIAO DIỆN ---
st.set_page_config(layout="wide", page_title="AI Studio V2")
st.title("📸 AI Product Studio (DreamShaper V8)")

# Khu vực trạng thái (Status Container)
with st.status("Hệ thống đang khởi động...", expanded=True) as status:
    try:
        pipe = load_models()
        status.update(label="✅ Hệ thống đã sẵn sàng!", state="complete", expanded=False)
    except Exception as e:
        st.error(f"Lỗi nghiêm trọng: {e}")
        status.update(label="❌ Khởi động thất bại", state="error")
        st.stop()

col1, col2 = st.columns(2)
with col1:
    f = st.file_uploader("Upload ảnh gốc", type=["jpg", "png"])
    if f: st.image(Image.open(f), caption="Ảnh gốc")

with col2:
    p = st.text_area("Mô tả bối cảnh:", "on a wooden table, sunlight, shadows")
    if st.button("🚀 TẠO ẢNH", type="primary") and f:
        with st.spinner("Đang vẽ... (Mất khoảng 10-15s)"):
            res = process_image(Image.open(f).convert("RGB"), p, "ugly, bad quality", pipe)
            st.image(res, caption="Kết quả")