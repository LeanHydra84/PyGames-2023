import pygame
import random as rand

min_leaf_size = 6
max_leaf_size = 20

class Node:
    def __init__(self, rect):

        self.leftchild = None
        self.rightChild = None

        self.room = None

        self.rect = pygame.Rect(rect)
        self.halls = []

    def split(self):
        if self.leftchild != None or self.rightChild != None:
            print("Already Split")
            return False
        
        horizontal = False
        if self.rect.w / self.rect.h > 1.25:
            horizontal = True
        if self.rect.h / self.rect.w > 1.25:
            horizontal = False
        else:
            horizontal = rand.choice([True, False])

        maxS = (self.rect.w if horizontal else self.rect.h) - min_leaf_size
        if maxS <= min_leaf_size:
            print("Too small")
            return False
        
        split = rand.randrange(min_leaf_size, maxS)
        if horizontal:
            self.leftchild = Node(pygame.Rect(self.rect.topleft, (self.rect.w, split)))
            self.rightChild = Node(pygame.Rect((self.rect.x, self.rect.y + split), (self.rect.w, self.rect.h - split)))
        else:
            self.leftchild = Node(pygame.Rect(self.rect.topleft, (split, self.rect.height)))
            self.rightChild = Node(pygame.Rect(self.rect.x + split, self.rect.y), (self.rect.w - split, self.rect.h))
        return True

def createmap(group):

    nodes = []
    root = Node(pygame.Rect(0, 0, 1280, 720))
    nodes.append(root)

    didsplit = True
    while didsplit:
        didsplit = False

        for l in nodes:
            if l.leftChild == None and l.rightChild == None:
                if l.rect.w > max_leaf_size or l.rect.h > max_leaf_size or (rand.random() > 0.25):
                    if l.split():
                        nodes.append(l.leftChild)
                        nodes.append(l.rightChild)
                        didsplit = True
    
    