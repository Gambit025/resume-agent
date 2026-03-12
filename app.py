"""
Flask 后端：LLM 驱动的简历格式转换。
"""
import os
import uuid
from flask import Flask, request, jsonify, send_file, send_from_directory

from llm_generator import generate_resume

app = Flask(__name__, static_folder="static", static_url_path="")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    resume_file = request.files.get("resume")
    template_file = request.files.get("template")

    if not resume_file or not template_file:
        return jsonify({"error": "请同时上传简历和模板文件"}), 400

    if not resume_file.filename.lower().endswith(".pdf") or not template_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "仅支持 PDF 格式"}), 400

    job_id = str(uuid.uuid4())[:8]
    job_dir = os.path.join(UPLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    resume_path = os.path.join(job_dir, "resume.pdf")
    template_path = os.path.join(job_dir, "template.pdf")

    try:
        resume_file.save(resume_path)
        template_file.save(template_path)

        result = generate_resume(resume_path, template_path, job_dir)

        return jsonify({
            "success": True,
            "job_id": job_id,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"处理失败：{str(e)}"}), 500


@app.route("/api/download/<job_id>")
def download(job_id):
    output_path = os.path.join(UPLOAD_DIR, job_id, "output.pdf")
    if not os.path.exists(output_path):
        return jsonify({"error": "文件不存在"}), 404
    return send_file(output_path, as_attachment=True, download_name="简历.pdf")


@app.route("/api/preview/<job_id>")
def preview(job_id):
    html_path = os.path.join(UPLOAD_DIR, job_id, "output.html")
    if not os.path.exists(html_path):
        return jsonify({"error": "文件不存在"}), 404
    return send_file(html_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
