Apple Ripeness Detector System based on Skin Colour Features with Convolutional Neural Network Model are a system that is meant to aid Apple Farmers, Distributors and Supermarkets to determine ripeness level of an apple based on its skin colour.
This system helps to replace conventional human labour and reduces human error due to perception difference towards deciding ripeness level of an apple based on its skin colour. This system uses Deep Learning Convolutional Neural Network to learn the characteristics of skin colour and predicts the ripeness level whicah are divided into three ripeness categories: Unripe, Half Ripe and Ripe.
To help the ease of use for end-user to predict the apple ripeness, localhost website Graphical User Interface are made using Flask which helps visualize all predicted apple ripeness using a historical table and comparison graphs which shows the amount of Unripe, Half Ripe and Ripe apples that has been predicted.
This system uses Raspberry Pi Model 3B+ which serves as the web server for localhost website and storing the CNN model. To start the ripeness prediction, pushbuttons are used to select the type of apple, Manalagi or Rome Beauty and a Pi Camera which captures the apple that's placed in front of the camera. Predicted Ripeness level then are displayed on I2C LCD and localhost website.