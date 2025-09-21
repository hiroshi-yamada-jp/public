"""
概要: FastAPI:File upload
動作: OK @2025/09/21
"""
# 標準ライブラリ
import os
import shutil
# 拡張ライブラリ
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse

# -------------------------
#  APIサーバ定義
# -------------------------
title = "FastAPI Binary file uploader"
description = """
"""
app = FastAPI(title=title, description=description, version="V1.0.0")


# ----------------------------------
#  API End Point定義
# ----------------------------------
@app.get("/", include_in_schema=True)
def redirect():
    """リダイレクト処理(Swagger UI表示)"""
    return RedirectResponse(url="/docs")


@app.post("/upload/")
def upload_file(file: UploadFile = File(default=...)):
    filename = file.filename
    content_type = file.content_type
    out_dir = "./out"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, file.filename)

    # ファイルの拡張子やMIMEタイプで処理を分岐
    if content_type.startswith("text/") or filename.endswith(".txt"):
        with open(out_file, "wt") as of:
            shutil.copyfileobj(file.file, of)
    else:
        with open(out_file, "wb") as of:
            shutil.copyfileobj(file.file, of)

    return JSONResponse(content={
        "filename": filename,
        "content_type": content_type,
        "file_size": os.path.getsize(out_file),
    })


# サーバ起動エントリ
if __name__ == '__main__':
    import uvicorn

    # 実行ファイル名から拡張子を除いたファイル名を取得し、appの起動名を生成する
    name = os.path.splitext(os.path.basename(__file__))[0]
    app_name = F"{name}:app"
    host = "localhost"  # 公開時: "0.0.0.0"
    uvicorn.run(app=app_name, host=host, port=8000, reload=True)
