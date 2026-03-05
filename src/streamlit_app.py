import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
ENDPOINT_URL = os.environ.get("HF_ENDPOINT_URL")

PROMPT_TEMPLATE = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    คุณเป็น AI ผู้เชี่ยวชาญด้านการตรวจสอบข่าวภาษาไทย กรุณาวิเคราะห์หัวข้อข่าวต่อไปนี้และตอบว่าเป็น "ข่าวจริง" หรือ "ข่าวปลอม" เท่านั้น

    ### Input:
    {}

    ### Response:
    """



st.set_page_config(
    page_title="Thai Fake News Detector",
    page_icon="🔍",
    layout="centered",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔗 ลิงก์โปรเจกต์")
    st.markdown(
        """
- 🤗 [HF Space](https://huggingface.co/spaces/thirdExec/thai_fakenews_detector)
- 💻 [Training Code](https://github.com/Thirdbot/FineTuneSloth)
- 🧠 [Model](https://huggingface.co/thirdExec/Qwen2.5-1.5B-Instruct-ThaiFakeNews-bnb-4bit)
- 📊 [Dataset](https://huggingface.co/datasets/EXt1/Thai-True-Fake-News)
"""
    )
    st.markdown("---")
    st.caption("Dataset: 6,004 Thai news articles (2017–2024) from Antifakenewscenter Thailand")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔍 ตรวจสอบข่าวปลอมภาษาไทย")
st.caption("Thai Fake News Detector · Powered by Qwen2.5-7B fine-tuned on Thai news")

st.info(
    "โมเดลนี้ใช้ **Qwen2.5-7B** ที่ผ่านการ fine-tune บนชุดข้อมูลข่าวภาษาไทย 6,004 บทความ "
    "เพื่อจำแนกว่าข่าวนั้นเป็น **ข่าวจริง (ข่าวจริง)** หรือ **ข่าวปลอม (ข่าวปลอม)**",
    icon="ℹ️",
)

# ── Input ─────────────────────────────────────────────────────────────────────
news_input = st.text_area(
    "ใส่หัวข้อข่าวหรือเนื้อหาข่าวที่ต้องการตรวจสอบ",
    placeholder="เช่น: รัฐบาลแจกเงินคนละ 10,000 บาท ผ่านแอปเป๋าตัง",
    height=160,
)

col1, col2 = st.columns([3, 1])
with col1:
    run = st.button("🔎 ตรวจสอบ", type="primary", use_container_width=True)
with col2:
    clear = st.button("🗑️ ล้าง", use_container_width=True)

if clear:
    st.rerun()

# ── Inference ─────────────────────────────────────────────────────────────────
if run:
    if not news_input.strip():
        st.warning("⚠️ กรุณาใส่ข้อความข่าวก่อนตรวจสอบ")
    else:
        with st.spinner("กำลังวิเคราะห์ข่าว…"):
            try:
                client = InferenceClient(base_url=ENDPOINT_URL, token=os.environ.get("HF_TOKEN"))

                prompt = PROMPT_TEMPLATE.format(news_input)

                response = client.text_generation(
                    prompt,
                    max_new_tokens=20,
                    temperature=0.05,
                    do_sample=True,
                )

                generated = response.split("### Response:")[-1].strip()

                is_fake = "ปลอม" in generated

                st.markdown("---")
                st.subheader("ผลการตรวจสอบ")

                if "จริง" in generated:
                    st.success(
                        "## ✅ ข่าวจริง\n\n"
                        "โมเดลประเมินว่าข่าวนี้มีแนวโน้มเป็น **ข่าวจริง**",
                    )
                elif "ปลอม" in generated:
                    st.error(
                        "## ❌ ข่าวปลอม\n\n"
                        "โมเดลประเมินว่าข่าวนี้มีแนวโน้มเป็น **ข่าวปลอม**",
                    )
                else:
                    st.error(
                        "## ❌ ไม่่สามารถวิเคราะห์ได้\n\n"

                    )

                with st.expander("ดูผลลัพธ์ดิบจากโมเดล"):
                    st.code(response, language=None)

            except Exception as exc:
                st.error(f"เกิดข้อผิดพลาด: {exc}")
                st.info(
                    "**แนวทางแก้ไข:**\n"
                    "- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต\n"
                    "- โมเดลอาจยังไม่พร้อมใช้งานผ่าน Inference API — "
                    "ลองเปิด [HF Space](https://huggingface.co/spaces/thirdExec/thai_fakenews_detector) แทน"
                )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "⚠️ ผลการตรวจสอบจากโมเดล AI อาจไม่ถูกต้องเสมอไป "
    "กรุณายืนยันจากแหล่งข่าวที่น่าเชื่อถือก่อนเผยแพร่ต่อเสมอ"
)