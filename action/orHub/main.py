from or2fastrunAdapter import OR






       
def main():
    orService = OR()
    orService.imports("d:/or/to.json")
    p = Browser("百度一下，你就知道").Page("百度一下，你就知道").WebButton("百度一下")
    ret1, ret2 = orService.getDescription(p)
    print(ret1)

if __name__ == "__main__":
    main()