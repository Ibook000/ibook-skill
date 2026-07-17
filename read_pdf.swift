import Foundation
import Quartz

func extractText(from pdfPath: String) {
    let url = URL(fileURLWithPath: pdfPath)
    if let pdf = PDFDocument(url: url) {
        let maxPages = min(pdf.pageCount, 3)
        for i in 0..<maxPages {
            if let page = pdf.page(at: i), let text = page.string {
                print("--- Page \(i+1) ---")
                print(text)
            }
        }
    } else {
        print("Could not open PDF: \(pdfPath)")
    }
}

print("=== PINOUT ===")
extractText(from: "pinout.pdf")
print("=== SCHEMATIC ===")
extractText(from: "schematic.pdf")
