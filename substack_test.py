from substack.data.profile import Profile
from substack.substack_core import SubStack


def main():
    # profile = Profile("empty")
    #
    # sub_stack = SubStack()
    # sub_stack.set_profile(profile)
    #
    # sub_stack.start()

    ports = [80, 60]
    print " ".join(str(ports))
    print ' '.join(str(x) for x in ports)

if __name__ == "__main__":
    main()
