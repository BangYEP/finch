import argparse

parser = argparse.ArgumentParser()

#parser.add_argument('--vocab_size', type=int, default=20000)
parser.add_argument('--num_sampled', type=int, default=1000)
parser.add_argument('--max_len', type=int, default=20)
parser.add_argument('--word_dropout_rate', type=float, default=0.5)
parser.add_argument('--batch_size', type=int, default=128)
parser.add_argument('--embedding_dim', type=int, default=128)
parser.add_argument('--rnn_cell', type=str, default='GRU')
parser.add_argument('--rnn_size', type=int, default=128)
parser.add_argument('--encoder_layers', type=int, default=2)
parser.add_argument('--decoder_layers', type=int, default=2)
parser.add_argument('--beam_width', type=int, default=5)
parser.add_argument('--clip_norm', type=float, default=5.0)
parser.add_argument('--latent_size', type=int, default=16)
parser.add_argument('--anneal_max', type=float, default=1.0)
parser.add_argument('--anneal_bias', type=int, default=10000)
parser.add_argument('--num_epoch', type=int, default=100)
parser.add_argument('--display_loss_step', type=int, default=50)

args = parser.parse_args()
