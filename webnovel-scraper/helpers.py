import pycountry


def is_iso_639_compliant(tag):
    try:
        # Check if the tag is in ISO 639-1 or ISO 639-3
        if pycountry.languages.get(alpha_2=tag) or pycountry.languages.get(alpha_3=tag):
            return True
        else:
            return False
    except:
        # If the tag is not found or an error occurs
        return False


# Example usage
tag = "nn"
print(is_iso_639_compliant(tag))  # Output: True if 'nn' is compliant, False otherwise
