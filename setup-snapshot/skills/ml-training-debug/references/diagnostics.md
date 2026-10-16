# Training diagnostics

Use the symptom to choose a discriminating observation before changing hyperparameters.

| Symptom | Check first | What the check does not establish |
| --- | --- | --- |
| Flat loss | Correct nonempty labels/masks, loss reduction, gradients, optimizer membership, update magnitude and learning rate | That more epochs or a larger model is needed |
| NaN/Inf | First nonfinite activation/loss/gradient, invalid targets, overflow, loss scaling, normalization denominators | That low precision alone is the cause |
| Tiny subset cannot be fit | Token/target alignment, frozen weights, train/eval modes, actual optimizer step, conflicting examples | Held-out generalization |
| Training improves, validation worsens | Duplicate/related examples, split construction, objective mismatch, model selection, regularization and data coverage | That the architecture is intrinsically unsuitable |
| Loss falls but repair does not improve | Label objective, patch format/application, retrieval coverage, behavioral checks, error categories | An adaptation benefit |
| Out of memory | Live tensors, retained graphs, activations at actual sequence/batch length, optimizer/quantization buffers, allocator measurements | That trainable-parameter count predicts total memory |
| Reloaded adapter differs | Base/tokenizer revision, module names, saved config, dtype, eval mode, merged/unmerged state | A need to retrain from scratch |
| Resume changes behavior | RNG/sampler/dataloader position, optimizer/scheduler/scaler state, nondeterministic kernels, checkpoint step semantics | Cross-platform bitwise reproducibility |

For an ordinary data-parallel update with equal full microbatches, effective examples/update = examples/device/microbatch × accumulation steps × data-parallel replicas. Variable lengths, partial batches, distributed loss averaging, and token-normalized objectives change the weighting; inspect actual supervised-token totals.

In causal language modeling, confirm whether the library shifts labels internally before adding a manual shift. Check packed-example attention boundaries and EOS handling. A packed sequence can unintentionally expose one example's answer to another.

Profiling records should include units, warmup, synchronization where required, hardware, sequence lengths, batch, precision, train/infer mode, peak allocated/reserved memory where available, and instrumentation overhead. Treat a rough analytical estimate as an estimate until measured.
