"""
CS370 Treasure Hunt - Enhanced Q-learning training function

This version keeps the original Q-learning training approach but adds
better tracking of each episode. The added history makes it easier to see
how many steps the agent takes, how often it explores versus exploits, and
how epsilon changes during training.
"""


def qtrain_enhanced(model, maze, **opt):
    # Keep the original exploration setting but allow it to be passed in.
    global epsilon
    epsilon = opt.get('epsilon_start', epsilon)
    epsilon_min = opt.get('epsilon_min', 0.05)
    epsilon_decay = opt.get('epsilon_decay', 0.995)

    n_epoch = opt.get('n_epoch', 15000)
    max_memory = opt.get('max_memory', 1000)
    data_size = opt.get('data_size', 50)
    target_update_freq = opt.get('target_update_freq', 50)

    start_time = datetime.datetime.now()
    qmaze = TreasureMaze(maze)

    target_model = clone_model(model)
    target_model.set_weights(model.get_weights())

    experience = GameExperience(
        model, target_model, max_memory=max_memory
    )

    win_history = []
    hsize = qmaze.maze.size // 2
    win_rate = 0.0
    loss = 0.0

    # New tracking data for the enhancement.
    training_history = []
    best_average_steps = None

    for epoch in range(n_epoch):
        free_cells = list(zip(*np.where(maze == 1)))
        start_cell = random.choice(free_cells)
        qmaze.reset(start_cell)
        env_state = qmaze.observe()
        game_over = False
        episode_steps = 0
        exploration_steps = 0
        exploitation_steps = 0

        while not game_over:
            prev_env_state = env_state
            valid_actions = qmaze.valid_actions()

            # Exploration tries a new valid action. Exploitation uses the
            # best action the model currently knows.
            if np.random.rand() < epsilon:
                action = random.choice(valid_actions)
                exploration_steps += 1
            else:
                q_values = experience.predict(prev_env_state)
                action = max(valid_actions, key=lambda x: q_values[x])
                exploitation_steps += 1

            env_state, reward, game_status = qmaze.act(action)
            episode_steps += 1

            if game_status == 'win':
                win_history.append(1)
                game_over = True
            elif game_status == 'lose':
                win_history.append(0)
                game_over = True

            episode = [
                prev_env_state,
                action,
                reward,
                env_state,
                game_status,
            ]
            experience.remember(episode)

            inputs, targets = experience.get_data(data_size)
            batch_loss = model.train_on_batch(inputs, targets)
            loss = batch_loss

        if epoch % target_update_freq == 0:
            target_model.set_weights(model.get_weights())

        win_rate = (
            sum(win_history[-hsize:]) / hsize
            if len(win_history) >= hsize
            else 0.0
        )

        # Calculate a moving average of steps so training can be evaluated
        # by more than just the win rate.
        recent_steps = [item['steps'] for item in training_history[-hsize:]]
        recent_steps.append(episode_steps)
        average_steps = sum(recent_steps) / len(recent_steps)

        if best_average_steps is None or average_steps < best_average_steps:
            best_average_steps = average_steps

        total_actions = exploration_steps + exploitation_steps
        exploration_rate = (
            exploration_steps / total_actions if total_actions else 0.0
        )
        exploitation_rate = (
            exploitation_steps / total_actions if total_actions else 0.0
        )

        training_history.append({
            'epoch': epoch,
            'steps': episode_steps,
            'average_steps': average_steps,
            'win_rate': win_rate,
            'epsilon': epsilon,
            'exploration_steps': exploration_steps,
            'exploitation_steps': exploitation_steps,
            'exploration_rate': exploration_rate,
            'exploitation_rate': exploitation_rate,
            'loss': float(loss),
        })

        dt = datetime.datetime.now() - start_time
        t = format_time(dt.total_seconds())

        print(
            "Epoch: {:03d}/{:d} | Loss: {:.4f} | Steps: {:d} | "
            "Avg steps: {:.2f} | Win rate: {:.3f} | Explore: {:.2f} | "
            "Exploit: {:.2f} | Epsilon: {:.3f} | time: {}".format(
                epoch,
                n_epoch - 1,
                float(loss),
                episode_steps,
                average_steps,
                win_rate,
                exploration_rate,
                exploitation_rate,
                epsilon,
                t,
            )
        )

        # Gradually move from exploration toward exploitation while still
        # keeping a small amount of exploration available.
        epsilon = max(epsilon * epsilon_decay, epsilon_min)

        if win_rate >= 0.999 and completion_check(model, maze):
            print(
                "Reached 100% win rate at epoch {} with an average of "
                "{:.2f} steps.".format(epoch, average_steps)
            )
            break

    total_time = format_time(
        (datetime.datetime.now() - start_time).total_seconds()
    )
    print("Training complete in:", total_time)

    # Return the history so it can be reviewed or plotted after training.
    return training_history
