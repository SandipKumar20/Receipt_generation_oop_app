import pandas as pd
from fpdf import FPDF

df = pd.read_csv("articles.csv", dtype={"id": str})

print(df)


class Article:
    def __init__(self, article_id):
        self.id = article_id
        self.name = df.loc[df["id"] == self.id, "name"].squeeze()
        self.price = df.loc[df["id"] == self.id, "price"].squeeze()

    def available(self):
        in_stock = df.loc[df["id"] == self.id, "in stock"].squeeze()
        return in_stock


class Receipt:
    def __init__(self, article):
        self.article = article

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=170, h=8, txt=f"Receipt nr.{self.article.id}", ln=3, align="C")

        pdf.set_font(family="Times", size=16, style="I")
        pdf.cell(w=170, h=8, txt=f"Article: {self.article.name}", ln=3, align="C")

        pdf.set_font(family="Times", size=16, style="U")
        pdf.cell(w=170, h=8, txt=f"Price: {self.article.price}", ln=3, align="C")
        pdf.output("receipt.pdf")


article_ID = input("Enter the id of the article you want to buy: ")
article = Article(article_id=article_ID)
if article.available():
    receipt = Receipt(article)
    receipt.generate()
    #stock = df.loc[df['id'] == '101', 'in stock'].squeeze()
    row_index = df.index[df['id'] == article_ID].tolist()[0]
    print(row_index)
    df.loc[row_index, "in stock"] = df.loc[row_index, "in stock"] - 1
    df.to_csv("articles.csv", index=False)
else:
    print("The article is out of stock.")

