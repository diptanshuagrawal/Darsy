import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("darsydutchman@gmail.com", "shashank123")
 
msg = "YOUR MESSAGEssssssss!"
server.sendmail("shashankgandham@gmail.com", "shashankgandham@gmail.com", msg)
server.quit()
