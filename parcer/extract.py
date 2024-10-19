import re

def split_plan(plan):
    group = dict()
    identifier_map = dict()
    all_identifiers = set()

    identifier_pattern = re.compile(r'#E\d+')

    for line in plan.split("\n"):
        if line:
            current_identifiers = set(re.findall(identifier_pattern, line))

            if not current_identifiers:
                continue

            # Find the original group for any identifier in the current line (e.g., #E10 -> #E4)
            original_identifier = None
            for identifier in current_identifiers:
                if identifier in identifier_map:
                    original_identifier = identifier_map[identifier]
                    break
                elif identifier in all_identifiers:
                    original_identifier = identifier
                    break

            if original_identifier:
                group[original_identifier].append(line)

                for identifier in current_identifiers:
                    identifier_map[identifier] = original_identifier
            else:
                # If no original identifier was found, create a new group for these identifiers
                first_identifier = next(iter(current_identifiers))
                group[first_identifier] = [line]
                all_identifiers.update(current_identifiers)

                # Map all these identifiers to this group
                for identifier in current_identifiers:
                    identifier_map[identifier] = first_identifier

    return group
