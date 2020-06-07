# get the contours
def contour_groups(image):

    contours, heirachy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    chain_list = [[]]
    point_list = []

    for c in contours:
        mask = np.zeros_like(image)

        for pt in c:
            chain_list[-1].append(pt[0])
        chain_list[-1].append(c[0][0])
        chain_list.append([])

        mask = cv2.drawContours(mask, [c], -1, 255, -1)

        masked_image = cv2.bitwise_and(image, mask)

        points = np.flip(np.array(np.where(masked_image == 255)).transpose())

        x = points.size
        for cp in chain_list[-2]:
            #print(cp,points[0], points.shape)
            points = points[(cp != points).any(axis=1)]
        # print(x, points.size)

        if len(points) > 0:
            point_list.append([])
            point_list[-1].append(points)
        #plt.imshow(cv2.drawContours(mask, [c], -1, 255, -1))
        #plt.show()
    # print(np.array(point_list).shape, point_list[0])
    return chain_list, point_list


def contour_groups_v2(image):
    # get the filled and unfilled areas of the image

    # if this is not done, there is the potential for overlap

    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    filled = []
    empty = []
    h_list = []
    chain_list = []

    previous = False

    for h in hierarchy[0]:
        h_list.append(list(h))


    mask = np.zeros_like(image)

    for x, c in enumerate(contours):
        h = h_list[x]
        # if there are no parents, this is an external contour
        if h[3] == -1:
            h_list[x].append(0)
        else:
            h_list[x].append(h_list[h_list[x][3]][4]+1)

        print(x,h_list[x])


        if h_list[x][4] % 2 == 1:
            mask = cv2.drawContours(mask, [c], 0, 0, -1)
            chain = np.flip(np.array(np.where(mask == 255)).transpose())
            chain_list.append(chain)
            mask = np.zeros_like(image)
        # even contours are filled space
        else:
            mask = cv2.drawContours(mask, [c], 0, 255, -1)

            # if the contour does not have children add the mask to points and reset
            if h_list[x][2] == -1:
                chain = np.flip(np.array(np.where(mask == 255)).transpose())
                chain_list.append(chain)
                mask = np.zeros_like(image)
    #print(chain_list)

    return chain_list
