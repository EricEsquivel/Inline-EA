BOFNAME := inline-ea
DIST_DIR := prebuilt
SRC_DIR := src
CC_x64 := x86_64-w64-mingw32-gcc
CC_x86 := i686-w64-mingw32-gcc

all:
	$(CC_x64) -o $(DIST_DIR)/$(BOFNAME).x64.o -Os -c $(SRC_DIR)/main.cpp
	$(CC_x86) -o $(DIST_DIR)/$(BOFNAME).x86.o -Os -c $(SRC_DIR)/main.cpp

clean:
	rm -f $(DIST_DIR)/*.o