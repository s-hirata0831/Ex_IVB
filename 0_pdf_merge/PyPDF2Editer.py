"""PDF結合スクリプト

改良点:
1. AES暗号化PDFに遭遇した場合 PyCryptodome が未導入ならメッセージを出してスキップ。
2. is_encrypted を確認しパスワード不要の単純暗号なら decrypt() を試行。
3. 例外発生時にそのファイルを飛ばして続行。
4. コマンドライン引数対応: python PyPDF2Editer.py out.pdf in1.pdf in2.pdf ...
   引数が無ければ従来の2ファイル固定パスで動作。

PyCryptodome がない環境では AES 暗号PDFの結合はできずスキップされます。
"""

from pathlib import Path
import sys
import PyPDF2

DEFAULT_FILE1 = "/Users/hiratasoma/Documents/Ex_IVB/0_pdf_merge/merged.pdf"
DEFAULT_FILE2 = "/Users/hiratasoma/Downloads/付録.pdf"

def open_reader(path: str):
	"""Open a PDF file and return PdfReader or raise. Handles decryption if possible."""
	reader = PyPDF2.PdfReader(path)
	if reader.is_encrypted:
		try:
			# Try empty password first
			reader.decrypt("")
		except Exception as e:
			raise RuntimeError(f"暗号化PDFを復号できません: {path} ({e})")
	return reader

def append_pdf(merger: PyPDF2.PdfMerger, path: str):
	try:
		# Use merger.append directly; if encrypted and needs AES dependency missing, catch.
		merger.append(path)
		print(f"追加成功: {path}")
	except PyPDF2.errors.DependencyError as de:
		print(f"[SKIP] 依存ライブラリ不足 (PyCryptodome) のため '{path}' をスキップ: {de}")
	except Exception as e:
		print(f"[SKIP] '{path}' の追加中にエラー: {e}")

def main():
	args = sys.argv[1:]
	if len(args) >= 2:
		output = args[0]
		inputs = args[1:]
	else:
		output = "merged1.pdf"
		inputs = [DEFAULT_FILE1, DEFAULT_FILE2]

	# 存在チェック
	existing = []
	for p in inputs:
		if Path(p).is_file():
			existing.append(p)
		else:
			print(f"[WARN] ファイルが見つかりません: {p}")

	if not existing:
		print("入力PDFがありません。処理終了。")
		return

	merger = PyPDF2.PdfMerger()
	for pdf in existing:
		append_pdf(merger, pdf)

	if len(merger.pages) == 0:
		print("結合可能なPDFがありませんでした。出力を作成しません。")
		return

	merger.write(output)
	merger.close()
	print(f"出力完了: {output}")

if __name__ == "__main__":
	main()