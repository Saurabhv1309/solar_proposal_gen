import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
import io
import datetime

def generate_page_one(name, address, capacity):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 1. Top Image Section (approx 50% of the page)
    try:
        # Ensure you have the image saved as 'background.jpg'
        c.drawImage("background.jpg", 0, height/2, width=width, height=height/2, preserveAspectRatio=False)
    except:
        c.setFillColor(HexColor("#dddddd"))
        c.rect(0, height/2, width, height/2, fill=1)
        c.setFillColor(black)
        c.drawCentredString(width/2, (height/2) + 100, "[Image Background Missing]")

    # 2. Middle Content Section (White Background)
    c.setFillColor(white)
    c.rect(0, 1.5*inch, width, (height/2) - 1.5*inch, fill=1)

    # Left Column: Branding
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.5*inch, height/2 - 1*inch, "Shri Swami Solar")
    c.setFillColor(HexColor("#999999"))
   # c.drawString(1.7*inch, height/2 - 1*inch, "ENERGY")
    
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    c.drawString(0.5*inch, height/2 - 1.8*inch, "Shri Swami Solar")
    c.drawString(0.5*inch, height/2 - 2.0*inch, "Pvt. Ltd.")
  #  c.drawString(0.5*inch, height/2 - 2.5*inch, "Proposal no SAMPLE-001")

    # Vertical Divider Line
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(2.8*inch, height/2 - 0.7*inch, 2.8*inch, 1.8*inch)

    # Right Column: Proposal Details
    c.setFont("Helvetica-Bold", 28)
    c.drawString(3.0*inch, height/2 - 1*inch, "SOLAR PROPOSAL")
    
    c.setFont("Helvetica", 14)
    c.drawString(3.0*inch, height/2 - 1.6*inch, f"ONGRID {capacity}")
    
    # Dynamic Date
    today = datetime.datetime.now().strftime("%d, %B %Y")
    c.drawRightString(width - 0.5*inch, height/2 - 1.6*inch, today)

    c.setFont("Helvetica", 12)
    c.drawString(3.0*inch, height/2 - 2.1*inch, f"Client name: {name}")
    
    # Address wrapping
    text_obj = c.beginText(3.0*inch, height/2 - 2.6*inch)
    text_obj.setFont("Helvetica", 11)
    text_obj.setLeading(14)
    text_obj.textLines(address)
    c.drawText(text_obj)

    # 3. Bottom Black Footer
    c.setFillColor(black)
    c.rect(0, 0, width, 1.5*inch, fill=1)
    
    c.setFillColor(white)
    c.setFont("Helvetica", 9)
    # Prepared by
    c.drawString(0.5*inch, 1.1*inch, "Prepared by:")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.5*inch, 0.8*inch, "Mr.Sudarshan Varade")
    
    # Prepared for
    c.setFont("Helvetica", 9)
    c.drawString(2.3*inch, 1.1*inch, "Prepared for:")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2.3*inch, 0.8*inch, f"Mr. {name.split()[0]}")

    # Generated on details
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 0.5*inch, 1.1*inch, "Generated on")
    c.drawRightString(width - 0.5*inch, 0.8*inch, f"{today} | 10:30AM")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- Streamlit UI ---
st.title("Solar Proposal Generator")
c_name = st.text_input("Client Name", "Ravi Mathur")
c_addr = st.text_area("Client Address", "4A, Spaced Out Cafe, Hauz Khas,\nNew Delhi, 110016")
c_cap = st.selectbox("Capacity", ["3KW", "5KW", "10KW"])

if st.button("Generate Page 1"):
    pdf = generate_page_one(c_name, c_addr, c_cap)
    st.download_button("Download Proposal", data=pdf, file_name="Proposal.pdf", mime="application/pdf")
