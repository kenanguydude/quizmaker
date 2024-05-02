import os
import sqlite3
import time

# connect to database
con = sqlite3.connect("quiz.db")
c = con.cursor()


def clear():
  """Clears console, makes it look nice"""
  os.system("clear")


def interface():
  """The Main menu"""

  # this loop goes on forever until the user quits
  # typing 'exit' at any point brings you back here
  while True:
    try:
      print(
          "Welcome to Quiz Maker.\n\n 1. Create a new quiz\n 2. Select a quiz\n 3. Exit"
      )

      nav = int(input())
      clear()

      # Create a new quiz
      if nav == 1:
        create()

      # Select a quiz
      elif nav == 2:
        select()

      # Exit
      elif nav == 3:
        con.close()
        quit()

      else:
        raise ValueError

    except ValueError:
      clear()
      print("Invalid input.")
      time.sleep(1)
      clear()


def create():
  """Create a quiz."""

  print("You can exit back to the menu at any time by typing 'exit'")
  user_input = 0
  try:

    # get name
    user_input = input("Enter the name of the quiz: ")
    if exit(user_input) is True:
      clear()
      return

    # boundary case: name is Blank!
    while user_input == "":
      clear()
      print("Your quiz needs a name!")
      user_input = input("Enter the name of the quiz: ")

      if exit(user_input) is True:
        clear()
        return

    name = user_input

    # check if quiz already exists
    sql = "SELECT * FROM quiz WHERE name = ?"
    c.execute(sql, (name, ))
    already_existing_name = c.fetchall()

    # quiz exists, sends user to menu
    if len(already_existing_name) != 0:
      print("Quiz already exists.")
      time.sleep(1)
      clear()
      return

    # get description (I don't mind if it's blank)
    user_input = input("Enter the description of the quiz: ")
    if exit(user_input) is True:
      clear()
      return

    description = user_input

    # insert into table
    sql2 = "INSERT INTO quiz (name, desc) VALUES (?, ?)"
    c.execute(sql2, (name, description))
    con.commit()
    clear()

    # get id for that quiz
    sql3 = "SELECT id FROM quiz WHERE name = ?"
    c.execute(sql3, (name, ))
    id = c.fetchall()
    id = id[0][0]

    x = 0  # number i use for the loop
    while True:

      # find if quiz has questions or not
      sql7 = "SELECT * FROM quiz_question WHERE quiz_id = ?"
      c.execute(sql7, (id, ))
      questions = c.fetchall()

      print(f"{name}")
      print("Type exit to stop at anytime.\n")

      print(f"Question {x+1}.\n")

      # get question
      user_input = input("Enter the question: ")

      # boundary case: Question is blank
      while user_input == "":
        print("The question can't be blank, Silly")
        user_input = input("Enter the question: ")

      if exit(user_input) is True:

        # if the quiz has questions, user goes back as normal
        if len(questions) != 0:
          clear()
          return

        # otherwise Boundary case time Woohoo
        print("Your quiz has no questions!\n")
        while True:
          user_input = input("Enter the question: ")
          if user_input == "":
            print("The question can't be blank, Silly")
          elif exit(user_input) is True:
            print("Your quiz STILL has no questions!")
          else:
            break

      question = user_input

      # get answer
      user_input = input("Enter the answer: ")

      while user_input == "":
        print("The answer can't be blank, Silly")
        user_input = input("Enter the question: ")
        print("\n")

      if exit(user_input) is True:

        # if the quiz has questions, user goes back as normal
        if len(questions) != 0:
          clear()
          return

        # otherwise Boundary case time Woohoo
        print("Your quiz has no questions!\n")
        while True:
          user_input = input("Enter the answer: ")
          if user_input == "":
            print("The answer can't be blank, Silly")
          elif exit(user_input) is True:
            print("Your quiz STILL has no questions!")
          else:
            break

      answer = user_input

      # put question and answer in question_table
      sql4 = "INSERT INTO question_table (question, answer) VALUES (?, ?)"
      c.execute(sql4, (question, answer))
      con.commit()

      # find id of that question
      sql5 = "SELECT id FROM question_table WHERE question = ?"
      c.execute(sql5, (question, ))
      id_question = c.fetchall()
      id_question = id_question[0][0]

      # assign question to quiz
      sql6 = "INSERT INTO quiz_question (quiz_id, question_id) VALUES (?, ?)"
      c.execute(sql6, (id, id_question))
      con.commit()

      user_input = input(
          "Press enter to keep adding questions, or type 'exit' to finish. ")

      if exit(user_input) is True:
        clear()
        return

      else:
        x += 1
        clear()
        # loop again !

  except Exception:
    if exit(user_input) is True:
      clear()
      return
    print("Invalid input.")
    time.sleep(2)
    clear()


def select():
  """Selects a quiz from database. You can take, delete, edit or view leaderboard."""
  print("You can exit back to the menu at any time by typing 'exit'")
  user_input = 0
  try:
    print("What quiz would you like to select?")

    # get quizzes
    query = "SELECT name FROM quiz"
    c.execute(query)
    quiz_rows = c.fetchall()
    for x, row in enumerate(quiz_rows):
      print(f"{x+1}. {row[0]}")

    # user inputs the quiz they want to select
    user_input = input("")
    user_input = int(user_input)

    # the selected quiz
    selected_quiz = quiz_rows[user_input - 1][0]

    # get id of quiz
    query = "SELECT id FROM quiz WHERE name = ?"
    c.execute(query, (selected_quiz, ))
    id = c.fetchall()

    # get description of quiz
    query = "SELECT desc FROM quiz WHERE name = ?"
    c.execute(query, (selected_quiz, ))
    desc = c.fetchall()

    clear()
    print(f'You have selected "{selected_quiz}".')
    print(f'"{desc[0][0]}"')

    print(
        " 1. Take quiz\n 2. Edit quiz\n 3. Delete quiz\n 4. View leaderboard\n 5. Back"
    )
    user_input = input("")
    user_input = int(user_input)

    clear()

    # take quiz
    if user_input == 1:
      score = 0

      print(f"You have selected to take the quiz '{selected_quiz}'.")

      # get all questions from quiz
      sql = "SELECT question_id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz WHERE name=?)"
      c.execute(sql, (selected_quiz, ))
      rows = c.fetchall()

      # print all questions one by one
      for x, row in enumerate(rows):
        clear()
        row = row[0]

        print(f"{selected_quiz}")
        print(f"Question {x+1}:\n")

        # find and print question
        sql2 = "SELECT question FROM question_table WHERE id=?"
        c.execute(sql2, (row, ))
        question = c.fetchall()
        print(*question[0])
        print("\n")

        # find answer
        sql3 = "SELECT answer FROM question_table WHERE id=?"
        c.execute(sql3, (row, ))
        answer = c.fetchall()

        # user guess
        user_input = input("Answer here: ")

        # correct
        if user_input.lower() == answer[0][0]:
          print("Correct!")
          a = input("Press enter to continue. ")
          score += 1

        # user wants to go back to menu
        elif exit(user_input) is True:
          clear()
          return

        # incorrect
        else:
          print(f"\nIncorrect. The correct answer was {answer[0][0]}.")
          a = input("Press enter to continue. ")

      # done
      clear()

      # print score and leaderboard here
      print(f"You have finished the quiz '{selected_quiz}'.")
      print(f"You got {score} out of {len(rows)} correct.\n")

      name = input(
          "What is your name? (leave blank if you don't want to add score to leaderboard):\n"
      )

      # get quiz id
      sql4 = "SELECT id FROM quiz WHERE name=?"
      c.execute(sql4, (selected_quiz, ))
      quiz_id = c.fetchall()

      # append score and name to leaderboard
      while True:
        if name != "":
          sql5 = "SELECT name FROM quiz_leaderboard WHERE name = ? AND quiz_id = ?"
          c.execute(sql5, (name, quiz_id[0][0]))
          name_exists = c.fetchall()

          # name doesn't exist
          if len(name_exists) == 0:
            sql6 = "INSERT INTO quiz_leaderboard (quiz_id, name, score) VALUES (?, ?, ?)"
            c.execute(sql6, (quiz_id[0][0], name, score))
            con.commit()
            break

          # name exists
          else:
            name = input(
                "Name already exists. Please enter another username: ")

        elif name == "":
          break

      clear()
      print(f"{selected_quiz} Leaderboard:\n\n")

      # get leaderboard for specific quiz
      sql7 = "SELECT name, score FROM quiz_leaderboard WHERE quiz_id = ? ORDER BY score DESC"
      c.execute(sql7, (quiz_id[0][0], ))
      rowsleaderboard = c.fetchall()

      print("NAME - SCORE\n")
      for x, row in enumerate(rowsleaderboard):
        print(f"{x+1}. {row[0]} - {row[1]}/{len(rows)}")

      a = input("\n\nPress enter to continue. ")
      clear()
      select()

    # edit quiz
    elif user_input == 2:
      print("You have selected to edit the quiz.")
      print("NOTE: Editing a quiz will clear the leaderboard.\n")

      # while loop so i can go back here
      while True:
        # get questions from quiz selected
        edit_sql = "SELECT question_id FROM quiz_question WHERE quiz_id = ?"
        c.execute(edit_sql, (id[0][0], ))
        question_ids = c.fetchall()

        print("What question would you like to edit?\n")
        user_input = ""
        question_list = []

        # print all da questions
        for x, row in enumerate(question_ids):
          try:
            row = row[0]

            # get question
            edit_sql2 = "SELECT question FROM question_table WHERE id = ?"
            c.execute(edit_sql2, (row, ))
            questions = c.fetchall()

            if questions != []:
              question_list.append(questions)
            print(f" {x+1}. {questions[0][0]}")
          except IndexError:
            continue

        user_input = input("")
        user_input = int(user_input)
        question_id = user_input

        # get da question
        edit_sql3 = "SELECT question FROM question_table WHERE id = ?"
        c.execute(edit_sql3, (question_ids[user_input - 1][0], ))
        question = c.fetchall()

        # get da answer
        edit_sql4 = "SELECT answer FROM question_table WHERE id = ?"
        c.execute(edit_sql4, (question_ids[user_input - 1][0], ))
        answer = c.fetchall()

        clear()

        print(f"Question: {question[0][0]}")
        print(f"Answer: {answer[0][0]}\n")

        print("What would you like to edit?")
        print(" 1. Question\n 2. Answer\n 3. Delete question\n 4. Back")

        user_input = input("")
        user_input = int(user_input)

        delete_quiz_lb_sql = "DELETE FROM quiz_leaderboard WHERE quiz_id = ?"

        clear()

        # edit question + clear leaderboard
        if user_input == 1:
          print("What would you like to change the question to?")
          print(f"Old question: {question[0][0]}")

          user_input = input("New question: ")

          # change question in table
          edit_sql5 = "UPDATE question_table SET question = ? WHERE question = ?"
          c.execute(edit_sql5, (
              user_input,
              question[0][0],
          ))
          con.commit()

          # clear leaderboard
          c.execute(delete_quiz_lb_sql, (id[0][0], ))
          con.commit()

          clear()

        # edit answer + clear leaderboard
        elif user_input == 2:
          print("What would you like to change the answer to?")
          print(f"Old answer: {answer[0][0]}")

          user_input = input("New answer: ")

          # change answer in table
          edit_sql6 = "UPDATE question_table SET answer = ? WHERE answer = ?"
          c.execute(edit_sql6, (
              user_input,
              answer[0][0],
          ))
          con.commit()

          # clear leaderboard
          c.execute(delete_quiz_lb_sql, (id[0][0], ))
          con.commit()

          clear()

        # delete question + clear leaderboard
        elif user_input == 3:

          # delete question from quiz
          edit_sql7 = "DELETE FROM quiz_question WHERE question_id = (SELECT id FROM question_table WHERE question = ?)"
          c.execute(edit_sql7, (question[0][0], ))
          con.commit()

          # delete question
          edit_sql8 = "DELETE FROM question_table WHERE question = ?"
          c.execute(edit_sql8, (question[0][0], ))
          con.commit()

          # clear leaderboard
          c.execute(delete_quiz_lb_sql, (id[0][0], ))
          con.commit()

          print("Question deleted.")
          time.sleep(2)

        # loops back to edit
        elif user_input == 4:
          pass

    # delete quiz
    elif user_input == 3:
      sure = input("Are you sure you want to delete this quiz? (y/n)\n")

      # yes
      if sure == "y":
        sql = "DELETE FROM quiz WHERE name=?"
        c.execute(sql, (selected_quiz, ))
        con.commit()
        clear()
        print("Quiz deleted successfully.")
        time.sleep(1)
        return

      # no
      elif sure == "n":
        clear()
        select()

      else:
        raise ValueError

    elif user_input == 4:

      # get leaderboard
      query = "SELECT name, score FROM quiz_leaderboard WHERE quiz_id = ? ORDER BY score DESC"
      c.execute(query, (id[0][0], ))
      leaderboard = c.fetchall()

      # get total number of questions
      query = "SELECT question_id FROM quiz_question WHERE quiz_id = ?"
      c.execute(query, (id[0][0], ))
      rows = c.fetchall()

      print(f"{selected_quiz} Leaderboard:\n\n")
      print("NAME - SCORE\n")

      # name - score/total questions
      for row in leaderboard:
        print(f"{row[0]} - {row[1]}/{len(rows)}")

      user_input = input("\nPress enter to continue. ")
      clear()
      select()

    elif user_input == 5:
      clear()
      select()

    else:
      raise ValueError

  except Exception:
    if exit(user_input) is True:
      clear()
      return

    print("Invalid input.")
    time.sleep(2)
    clear()


def exit(input):
  """If user input is ever 'exit', should bring back user to menu"""
  if str(input).lower() == "exit":
    return True


interface()
