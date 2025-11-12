import PyPDF2

file1 = "/Users/hiratasoma/Documents/Ex_IVB/2_power/repo/power_front.pdf"
file2 = "/Users/hiratasoma/Documents/Ex_IVB/2_power/repo/power.pdf"

merger = PyPDF2.PdfMerger()
merger.append(file1)
merger.append(file2)

merger.write("merged.pdf")
merger.close()