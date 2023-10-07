**Title: Serverless Transaction Analyzer**

Description: This project is a Serverless Transaction Analyzer that provides insights into financial data. It includes a web interface where users can enter content, which triggers backend processes, and displays transaction statistics and a pie chart of transaction categories. Built using AWS Lambda, it offers a serverless and scalable solution.

![Screenshot 1](https://cdn.discordapp.com/attachments/359470187088576514/1160302301903331358/image.png?ex=65342aba&is=6521b5ba&hm=84b0fa3ada19544d4f4093ade4f7cd8feee99973998e961de1268edf784bb1a1)
![Screenshot 2](https://cdn.discordapp.com/attachments/359470187088576514/1160302302125637712/image.png?ex=65342aba&is=6521b5ba&hm=790d38bbdb80845f799b3a42ce53809e905ad2a17b4dc47a818858dbd1cf0e39)
![Screenshot 3](https://cdn.discordapp.com/attachments/359470187088576514/1160303365503340594/image.png?ex=65342bb7&is=6521b6b7&hm=b48f48ead78b88c101e4aa12f1f86da4ca915ad3b176e792d0b49cc119b7a055&)

**API Endpoints:**

1. Httml: [Link](https://518julmqj9.execute-api.us-east-1.amazonaws.com/default/create_file_s3)
2. Transactions Functions: [Link](https://0mmcz2p1dh.execute-api.us-east-1.amazonaws.com/default/count_transactions)

This project allows users to input content, which is processed by the serverless backend powered by AWS Lambda. The transaction data in CSV format is stored in Amazon S3 and retrieved for processing. The application then displays transaction details and categories in a user-friendly manner through the provided API endpoints.
