import PyPDF2

file1 = "/Users/hiratasoma/Documents/Ex_IVB/1_web_security/repo/web_security_front.pdf"
file2 = "/Users/hiratasoma/Documents/Ex_IVB/1_web_security/repo/web_security.pdf"

merger = PyPDF2.PdfMerger()
merger.append(file1)
merger.append(file2)

merger.write("merged.pdf")
merger.close()