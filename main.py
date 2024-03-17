import os
import time
import sqlite3

con = sqlite3.connect("quiz.db")
c = con.cursor()


def clear():
  os.system("clear")


def interface():
  """The main menu."""
  while True:
    try:
      print(
          "Welcome to Quiz Maker.\n 1. Create a new quiz\n 2. Select a quiz\n 3. Exit"
      )
      nav = int(input(""))
      clear()
      if nav == 1:
        create()
      elif nav == 2:
        select()
      elif nav == 3:
        quit()
      else:
        raise ValueError

    except ValueError:
      clear()
      print("Invalid input.")
      time.sleep(1)
      clear()


# edit quiz


def create():
  """Create a quiz."""
  print("You can exit back to the menu at any time by typing 'exit'")
  user_input = 0
  try:
    # get name
    user_input = input("Enter the name of the quiz: ")
    if user_input == "exit":
      clear()
      return

    name = user_input

    # check if quiz already exists
    sql = "SELECT * FROM quiz WHERE name = ?"
    c.execute(sql, (name, ))
    already_existing_name = c.fetchall()

    # quiz exists, user start again
    if len(already_existing_name) != 0:
      print("Quiz already exists.")
      time.sleep(1)
      clear()
      create()

    # get description
    user_input = input("Enter the description of the quiz: ")
    if user_input == "exit":
      clear()
      return

    description = user_input

    # insert into table
    sql2 = "INSERT INTO quiz (name, desc) VALUES (?, ?)"
    c.execute(sql2, (name, description))
    con.commit()  # ?
    clear()

    # get id for that quiz
    sql3 = "SELECT id FROM quiz WHERE name = ?"
    c.execute(sql3, (name, ))
    id = c.fetchall()
    id = id[0][0]

    x = 0
    while True:
      print(f"{name}")
      print(
          "Type exit to completely stop. Type stop the quiz at this question.\n"
      )

      print(f"Question {x+1}.\n")
      # get question
      user_input = input("Enter the question: ")
      if user_input == "exit":
        clear()
        return
      elif user_input == "stop":
        clear()
        break

      question = user_input

      # get answer
      user_input = input("Enter the answer: ")
      if user_input == "exit":
        clear()
        return
      elif user_input == "stop":
        clear()
        break

      answer = user_input

      # put question in question_table
      sql4 = "INSERT INTO question_table (question, answer) VALUES (?, ?)"
      c.execute(sql4, (question, answer))
      con.commit()

      # find id of that question
      sql5 = "SELECT id FROM question_table WHERE question = ?"
      c.execute(sql5, (question, ))
      id_question = c.fetchall()
      id_question = id_question[0][0]

      # put question in quiz
      sql6 = "INSERT INTO quiz_question (quiz_id, question_id) VALUES (?, ?)"
      c.execute(sql6, (id, id_question))
      con.commit()

      user_input = input(
          "Press enter to keep adding questions, or type 'stop' to finish. ")

      if user_input == "exit" or user_input == "stop":
        clear()
        break

      else:
        x += 1
        clear()
        pass

    return

  except Exception as e:
    if exit(user_input) == True:
      clear()
      return
    print("Invalid input.")
    print(e)
    a = input("Press enter to continue. ")

  # TO DO
  # multi answered questions
  # ask for correct answers in case of multi answer
  # delete quiz if quiz has 0 questions


def select():
  """Selects a quiz from the database. Take it, delete it, edit it or view the leaderboard."""
  print("You can exit back to the menu at any time by typing 'exit'")
  user_input = 0
  try:
    x = 0  # number i use for for loops

    print("What quiz would you like to select?")

    # get quizzes
    query = "SELECT name FROM quiz"
    c.execute(query)
    quiz_rows = c.fetchall()
    for row in quiz_rows:
      print(f"{x+1}. {row[0]}")
      x += 1
    x = 0

    # user inputs the quiz they want to select
    user_input = input("")
    user_input = int(user_input)

    # the selected quiz
    selected_quiz = quiz_rows[user_input - 1][0]

    query = "SELECT id FROM quiz WHERE name = ?"
    c.execute(query, (selected_quiz, ))
    id = c.fetchall()
    
    query = "SELECT desc FROM quiz WHERE name = ?"
    c.execute(query, (selected_quiz, ))
    desc = c.fetchall()

    clear()
    print(f'You have selected "{selected_quiz}".')
    print(f'"{desc[0][0]}"')

    print(" 1. Take quiz\n 2. Edit quiz\n 3. Delete quiz\n 4. View leaderboard\n 5. Back")
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
      for row in rows:
        clear()
        row = row[0]

        print(f"{selected_quiz}")
        print(f"Question {x+1}:\n")
        x += 1

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

        elif user_input == "exit":
          clear()
          return

        # incorrect
        else:
          print(f"\nIncorrect. The correct answer was {answer[0][0]}.")
          a = input("Press enter to continue. ")

      # done
      x = 0
      clear()

      # print score and leaderboard here (at some point)
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
      for row in rowsleaderboard:
        print(f"{x+1}. {row[0]} - {row[1]}/{len(rows)}")
        x += 1
      x = 0

      a = input("\n\nPress enter to continue. ")
      clear()
      select()

    # edit quiz
    elif user_input == 2:
      pass

    # delete quiz
    elif user_input == 3:
      sure = input("Are you sure you want to delete this quiz? (y/n)\n")

      # yes
      if sure == "y":
        sql = "DELETE FROM quiz WHERE name=?"
        c.execute(sql, (quiz_rows[user_input - 1][0], ))
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

    # TO DO
    # make sure user input is valid (?)
    # print leaderboard and add user to leaderboard
    # edit quizzes
    # print leaderboard from selection

  except Exception as e:
    # clear()
    if exit(user_input) is True:
      clear()
      return
    print("Invalid input.")
    print(e)
    a = input("Press enter to continue.")
    clear()
    select()


def exit(input):
  if str(input).lower() == "exit":
    return True

interface()
