## Scripts

- `mirror_data.sh`
    - a oneliner to rsync the direct-uploaded data (`/mnt/ubna_data_01`) to the other hard drive (`/mnt/ubna_data_01_mir`)
    - this script is run everyday at 2100 via crobjob:
        run 
        ```
        $ crontab -e
        ```
        and put in the following:
        ```
        MAILTO=example@email.com
        0 21 * * * PATH_TO_REPO/scripts/mirror_data.sh
        ```
