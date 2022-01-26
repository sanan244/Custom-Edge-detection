# Display greyscale data
"""
print("###############################################")
print("###############################################")
print("Data for Grey Image...")
# convert to greyscale
greyframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
for f in greyframe:
    print("Length of 1 sub array:", len(f))
    break

# Output Data
np_frame = np.array(frame)
print("Length of Raw Data: ", len(greyframe))
np.set_printoptions(threshold=np.inf, linewidth=1000)
#print("Raw Data:\n", greyframe)

# Display
# cv2.imshow('Frames', frame)
#plt.matshow(greyframe)
# plt.show()

# Process data
print("###############################################")
print("###############################################")
print("Data for Processed Image...")
#shape = process(greyframe)

# display
#plt.matshow(shape)
#plt.show()
"""