import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log.settings')  # Remplacez 'your_project' par le nom de votre projet
django.setup()

from camps.models import Camp 

def create_deadline():
    for camp in Camp.objects.all():
        if camp.branche != 'BP':
            camp.grille_ddcs_deadline = '23 mars'
            camp.save()
            print(f"DL créé pour {camp}")

def create_mail():
    for camp in Camp.objects.all():
        camp.mail= 'camp.' + camp.numero.replace(' ','').lower() + '@eeif.org'
        camp.save()
        print(f"Mail créé pour {camp}")

drive_links_BM = [
    "https://drive.google.com/drive/folders/1WW9-A5_lfkeMfuri-jQUzrMH47tHd6To?usp=share_link",
    "https://drive.google.com/drive/folders/1Iu2Lzi8W24VTrkYpCoNxD2yxByNFDv6V?usp=share_link",
    "https://drive.google.com/drive/folders/1UkvjGpEYeftQPBje8BtCmBvbCvrwu1CU?usp=share_link",
    "https://drive.google.com/drive/folders/1yURc9uDRcmkz60gL2aAUrdJ0c0L2sgqQ?usp=share_link",
    "https://drive.google.com/drive/folders/1B2XzF41ABPjOfvTHdiZ7Bv922r4IhrI1?usp=share_link",
    "https://drive.google.com/drive/folders/14uMskT1ToecDzRVW-eBZBeSiG8_hUYTt?usp=share_link",
    "https://drive.google.com/drive/folders/11apk-YTYLhf2unuOseCVjsErCz-DKVVB?usp=share_link",
    "https://drive.google.com/drive/folders/1j4Wk0NoyeK9nUbPpTp8dsuuZbmm7_hYT?usp=share_link",
    "https://drive.google.com/drive/folders/1U4b3FcoESq4NqpB4LmBaEg6BBEW-Qw0b?usp=share_link",
    "https://drive.google.com/drive/folders/1nSKIYWkypPEKGj08illrvwaKQlC7HYpI?usp=share_link",
    "https://drive.google.com/drive/folders/1MJnzXkKe-_mGsRZosBb1ym7EtRTR16SB?usp=share_link",
    "https://drive.google.com/drive/folders/1Etav9_-dLOzGgg0SDhOvF5HOAb31qB1a?usp=share_link",
    "https://drive.google.com/drive/folders/1U5ANzLZv0kX0jGeNSLJ5GbjI-d24X83m?usp=share_link",
    "https://drive.google.com/drive/folders/1g_EOvAlJ04zHebYyFemo0vpK5zrYwV1W?usp=share_link",
    "https://drive.google.com/drive/folders/1fIETIKV8jkAjxliFHjjxEtWQzPOw1sIl?usp=share_link",
    "https://drive.google.com/drive/folders/1IdtUT1XwdZYpoD8f8Z2yS0vJ38GEdHZR?usp=share_link",
    "https://drive.google.com/drive/folders/18gF9s-Xz1Hu1PWXpsEo26QO5gFLsKhE7?usp=share_link",
    "https://drive.google.com/drive/folders/1jT2GvBKtN1g3gCT3X2sdtRwOQlS1KQME?usp=share_link",
    "https://drive.google.com/drive/folders/1bDNPscmGkpcL6RfaABxJur8epWXkQR6i?usp=share_link",
    "https://drive.google.com/drive/folders/1-x7OQ3z7jzhsG6bfTt1GOsPHkrGnQwug?usp=share_link",
    "https://drive.google.com/drive/folders/1lqL0un-_FFIbbEVxOMPI7TfW6YqVdl5P?usp=share_link",
    "https://drive.google.com/drive/folders/1jrAfnMGJvWMzdgkKqlDqgxuEJFdVFFAu?usp=share_link",
    "https://drive.google.com/drive/folders/1M2hSRFboLQNcX4rU4mYxjPZDANQ-FO7T?usp=share_link",
    "https://drive.google.com/drive/folders/1ecHKWPC0uKBc567sUOEQ7TkwnPluAykd?usp=share_link"
]

drive_links_BC = [
    "https://drive.google.com/drive/folders/1z07fddVeZNubMaf76hvFwWyXZaVGQ6-g?usp=share_link",
    "https://drive.google.com/drive/folders/1FBlcQCyuLLuvap3qY0gavH-LrZG-t5pn?usp=share_link",
    "https://drive.google.com/drive/folders/1rbCWOsoquoJbAgL0snrPIkB0TG37w3dn?usp=share_link",
    "https://drive.google.com/drive/folders/1pNlz5UXoz7thBobKfUAYSqXYO08q4zdD?usp=share_link",
    "https://drive.google.com/drive/folders/1ZOD51l8954gtvcWXtXK1PPNI6c-brIsG?usp=share_link",
    "https://drive.google.com/drive/folders/1326N7cvmZ_31tP8z7jzUfgFeELGpplZH?usp=share_link",
    "https://drive.google.com/drive/folders/1bMZ6DrtHOc2BL8ZowVQjQVQ83iM_MQ_B?usp=share_link",
    "https://drive.google.com/drive/folders/1qiYtPe5h0r33Z-EaFuoOYzUtRbZoimln?usp=share_link",
    "https://drive.google.com/drive/folders/1MytUAyycrBDlVnVROPfdk8xz6dWhjOoA?usp=share_link",
    "https://drive.google.com/drive/folders/1SXuJSyU9q0-hFnYEEZuoc4gPDmi8KvrD?usp=share_link",
    "https://drive.google.com/drive/folders/1W1__6qvlwL_mgpq0jKX8-TjbT55rokuX?usp=share_link",
    "https://drive.google.com/drive/folders/1zRfTr3gaIATuQKo6dshkUtcipaYDXFsj?usp=share_link",
    "https://drive.google.com/drive/folders/18KED5eheOMb61LxhMumMrxR5KLaPIRo7?usp=share_link",
    "https://drive.google.com/drive/folders/1XCBh--eUkQM6JMFqVyFTs0nXhkF56OOT?usp=share_link",
    "https://drive.google.com/drive/folders/1LC0T-dVAtWaLVTPc9hzcBNFNeeDnPRgz?usp=share_link",
    "https://drive.google.com/drive/folders/1j2p0IBVy_AHF4RSfBTdrBqQpyweNoNO5?usp=share_link",
    "https://drive.google.com/drive/folders/1cfMIVDKuxczQ921M1d8XBxr5FmH_5mH6?usp=share_link"
]


def add_link():
    for camp in Camp.objects.all():
        if camp.branche == 'BC':
            camp.drive = drive_links_BC.pop(0)
            camp.save()
            print(f"Link ajouté pour {camp}")

create_deadline()