from goniometer_obj import GoniometerObject


def main():
    go = GoniometerObject()
    go.polarizer_angle = 15
    go.done_moving(go.POLARIZER)
    print("done")
    go.BP.reset_all()

    
if __name__ == '__main__':
    main()
