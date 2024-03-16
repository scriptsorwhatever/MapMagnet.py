def main():
    output_type = 'database'  # default output type
    output_file = ''

    while True:
        user_choice = main_menu()

        if user_choice == '1':
            output_type = 'database'
            logging.info("Output set to SQL Database.")
            connection = create_server_connection()
            if connection is None:
                continue

        elif user_choice == '2':
            output_type = 'file'
            output_file = input("Enter the output file name: ")
            logging.info(f"Output set to file: {output_file}. Note: Duplication detection is not performed when outputting to a text file.")

        elif user_choice.lower() == 'q':
            logging.info("Exiting program.")
            break

        search_choice = search_menu()
        if search_choice == '1':
            city = input("Enter city: ")
            keywords_input = input("Enter keywords separated by commas: ")
            keywords = [keyword.strip() for keyword in keywords_input.split(',')]

            total_added = 0
            total_duplicates = 0

            for keyword in keywords:
                logging.info(f"\nProcessing keyword: {keyword}")
                results = search_google_maps(keyword, city)

                for name, address, phone, place_id in results:
                    if output_type == 'database':
                        if not check_duplicate(connection, place_id):
                            query = f"INSERT INTO {table} (name, address, phone, place_id) VALUES (%s, %s, %s, %s);"
                            params = (name, address, phone, place_id)
                            execute_query(connection, query, params)
                            total_added += 1
                        else:
                            total_duplicates += 1

                    elif output_type == 'file':
                        with open(output_file, 'a') as f:
                            f.write(f"{name}, {address}, {phone}, {place_id}\n")
                            total_added += 1

                print(f"\r\033[32mHits {total_added}\033[0m - \033[31mDuplicates {total_duplicates}\033[0m", end='')

            logging.info("\nQuery complete")

        elif search_choice.lower() == 'b':
            continue
