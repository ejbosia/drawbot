#2020-05-30
np.where(array==0) can be used to find the locations of the black pixels in an image. The output is a tuple of each axis.

This can be converted into an array of points by using the np.array function on the np.where, and then applying the transpose function on the array:

np.array(np.where(array==0)).transpose()

I am not entirely sure how to combine like areas together yet but that will be the next step.
