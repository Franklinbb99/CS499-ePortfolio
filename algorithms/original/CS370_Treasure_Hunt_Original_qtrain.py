def qtrain(model, maze, **opt):
    # exploration factor
    global epsilon 
    
    # Number of epochs
    n_epoch = opt.get('n_epoch', 15000)
    
    # Maximum meory to store episodes
    max_memory = opt.get('max_memory', 1000)
    
    # Maximum data size for training
    data_size = opt.get('data_size', 50)
    
    # Frequency of target network updates
    target_update_freq = opt.get('target_update_freq', 50)
    
    # Start time
    start_time = datetime.datetime.now()
    
    # Construct environment/game from numpy array: maze (see argument above)
    qmaze = TreasureMaze(maze)
    
    # Target Network to better guide training
    target_model = clone_model(model)
    target_model.set_weights(model.get_weights())
    
    # Initialize experience replay object
    experience = GameExperience(model, target_model, max_memory=max_memory)

    win_history = [] # history of win/lose game
    hsize = qmaze.maze.size // 2 #history window size
    win_rate = 0.0
    
# =============START_HERE================
    loss = 0.0
    n_episodes = 0

    for epoch in range(n_epoch):

        # pick a random free cell (value = 1)
        free_cells = list(zip(*np.where(maze == 1)))
        start_cell = random.choice(free_cells)

        qmaze.reset(start_cell)

        # Get initial state
        env_state = qmaze.observe()

        game_over = False
        n_episodes += 1

        while not game_over:

            # Save previous state
            prev_env_state = env_state

            # Get valid actions
            valid_actions = qmaze.valid_actions()

            # Decide action (explore vs exploit)
            if np.random.rand() < epsilon:
                action = random.choice(valid_actions)
            else:
                q_values = experience.predict(prev_env_state)
                action = max(valid_actions, key=lambda x: q_values[x])

            # Take action
            env_state, reward, game_status = qmaze.act(action)

            # Check if game ended
            if game_status == 'win':
                win_history.append(1)
                game_over = True
            elif game_status == 'lose':
                win_history.append(0)
                game_over = True

            # Store episode in memory
            episode = [prev_env_state, action, reward, env_state, game_status]
            experience.remember(episode)

            # Train model
            inputs, targets = experience.get_data(data_size)
            batch_loss = model.train_on_batch(inputs, targets)
            loss = batch_loss

        # Update target model
        if epoch % target_update_freq == 0:
            target_model.set_weights(model.get_weights())

        # Win rate calculation
        win_rate = sum(win_history[-hsize:]) / hsize if len(win_history) >= hsize else 0.0

        # Print progress
        dt = datetime.datetime.now() - start_time
        t = format_time(dt.total_seconds())

        print("Epoch: {:03d}/{:d} | Loss: {:.4f} | Episodes: {:d} | Win count: {:d} | Win rate: {:.3f} | time: {}".format(
            epoch, n_epoch-1, loss, n_episodes, sum(win_history), win_rate, t))

        # Adjust epsilon
        if win_rate > 0.9:
            epsilon = 0.05
        else:
            epsilon = max(epsilon * epsilon_decay, epsilon_min)

        # Stop condition
        if win_rate >= 0.999 and completion_check(model, maze):
            print(f"Reached 100% win rate at epoch {epoch}")
            break

    total_time = format_time((datetime.datetime.now() - start_time).total_seconds())
    print("Training complete in:", total_time)


# This is a small utility for printing readable time strings:
def format_time(seconds):
    if seconds < 400:
        s = float(seconds)
        return "%.1f seconds" % (s,)
    elif seconds < 4000:
        m = seconds / 60.0
        return "%.2f minutes" % (m,)
    else:
        h = seconds / 3600.0
        return "%.2f hours" % (h,)
