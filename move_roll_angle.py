from goniometer_obj import GoniometerObject


def main():
    go = GoniometerObject()
    #print(go.sample_angle)
    go.roll_angle = 15
    go.done_moving(go.ROLL)
    print("done")
    go.BP.reset_all()

    
if __name__ == '__main__':
    main()