import yfinance as yf
import pandas as pd

# Define the stock symbol and time period
stock_symbol = 'AAPL'
start_date = '2012-01-01'
end_date = '2023-01-01'

# Fetch the data
stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

# Save the data to a CSV file
stock_data.to_csv(f'{stock_symbol}_stock_data.csv')

print(f"Data for {stock_symbol} saved successfully!")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot

df=pd.read_csv('AAPL_stock_data.csv')

df.head()

df.describe()

df.isnull().sum()

df.shape

df.head()

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.metrics import mean_squared_error, r2_score


# Convert 'Date' column to datetime and set as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Use only the 'Close' price for LSTM prediction
data = df[['Close']]

# Preprocessing: Scale the data to the range (0, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Create training and test sets (80% training, 20% test)
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

# Function to create the dataset for LSTM model (with look_back window)
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        X.append(dataset[i:(i + look_back), 0])
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# Hyperparameter: Look-back window
look_back = 60

# Create train and test datasets
X_train, Y_train = create_dataset(train_data, look_back)
X_test, Y_test = create_dataset(test_data, look_back)

# Reshape data for LSTM model (samples, time steps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(look_back, 1)))
model.add(LSTM(units=50))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, Y_train, epochs=10, batch_size=64)

# Make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse transform the scaled data back to original values
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset (already cleaned)
df = pd.read_csv('AAPL_stock_data.csv')
# Convert 'Date' column to datetime and set it as index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Use only the 'Close' price for prediction
data = df[['Close']]

# Preprocessing: Scaling the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Create the training dataset
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

# Function to create X and Y for LSTM
def create_dataset(dataset, look_back=60):
    X, Y = [], []
    for i in range(look_back, len(dataset)):
        X.append(dataset[i - look_back:i, 0])
        Y.append(dataset[i, 0])
    return np.array(X), np.array(Y)

look_back = 60  # Try experimenting with other values like 30, 100
X_train, Y_train = create_dataset(train_data, look_back)
X_test, Y_test = create_dataset(test_data, look_back)

# Reshape X to be [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build the LSTM model with Dropout to avoid overfitting
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))  # Dropout layer to reduce overfitting
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))  # Another Dropout layer
model.add(Dense(units=25))  # Dense layer
model.add(Dense(units=1))  # Output layer for prediction

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train, Y_train, epochs=15, batch_size=32, validation_data=(X_test, Y_test))

# Predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse scaling to original values
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# Inverse scale Y_train and Y_test
Y_train = scaler.inverse_transform([Y_train])
Y_test = scaler.inverse_transform([Y_test])

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(df.index[look_back:train_size], Y_train.flatten(), label='Training True')
plt.plot(df.index[train_size + look_back:], Y_test.flatten(), label='Testing True')
plt.plot(df.index[look_back:train_size], train_predict.flatten(), label='Training Predicted')
plt.plot(df.index[train_size + look_back:], test_predict.flatten(), label='Testing Predicted')
plt.title('LSTM Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Evaluate the model
mse = mean_squared_error(Y_test.flatten(), test_predict.flatten())
r2 = r2_score(Y_test.flatten(), test_predict.flatten())

print(f'Mean Squared Error: {mse}')
print(f'R-Squared: {r2}')

# Plot the results with years on the x-axis and Close Price on the y-axis
import matplotlib.dates as mdates

plt.figure(figsize=(12, 6))

# Plotting the training data
plt.plot(df.index[look_back:train_size], Y_train.flatten(), label='Training True', color='blue')
plt.plot(df.index[train_size + look_back:], Y_test.flatten(), label='Testing True', color='orange')

# Plotting the predicted data
plt.plot(df.index[look_back:train_size], train_predict.flatten(), label='Training Predicted', color='green')
plt.plot(df.index[train_size + look_back:], test_predict.flatten(), label='Testing Predicted', color='red')

# Formatting the date on the x-axis to show years
plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Show years
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format the x-axis to display the year

# Adding labels and title
plt.title('LSTM Stock Price Prediction')
plt.xlabel('Date (Year)')
plt.ylabel('Close Price (USD)')
plt.legend()

# Rotating the x-axis dates for better readability
plt.gcf().autofmt_xdate()

# Show the plot
plt.show()
