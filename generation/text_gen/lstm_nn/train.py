import numpy as np
import torch
import torch.nn as nn

from models import TextRNN
from preprocessing_data import idx_to_word, get_batch, sequence, BATCH_SIZE, evaluate, word_to_idx, device


model = TextRNN(input_size=len(idx_to_word),
                       hidden_size=128,
                       embedding_size=128,
                       n_layers=2)
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-6, amsgrad=True)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    patience=5,
    verbose=True,
    factor=0.5
)

n_epochs = 50000
loss_avg = []

for epoch in range(n_epochs):
    model.train()
    train, target = get_batch(sequence)
    train = train.permute(1, 0, 2).to(device)
    target = target.permute(1, 0, 2).to(device)
    hidden = model.init_hidden(BATCH_SIZE)

    output, hidden = model(train, hidden)
    loss = criterion(output.permute(1, 2, 0), target.squeeze(-1).permute(1, 0))

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    loss_avg.append(loss.item())
    #     if len(loss_avg) >= 50:
    mean_loss = np.mean(loss_avg)
    print(f'\nn_epochs: {epoch}')
    print(f'Loss: {mean_loss}')
    scheduler.step(mean_loss)
    loss_avg = []
    model.eval()
    predicted_text = evaluate(model,
                              word_to_idx,
                              idx_to_word)
    print(predicted_text)


# save
PATH_to_model = 'generation/text_gen/lstm_nn/weight/model_all'
PATH_to_weight = 'generation/text_gen/lstm_nn/weight/weight_model'

torch.save(model, PATH_to_model)
torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss
            }, PATH_to_weight)



