def generate_streams(count, periods, network, frame_counts):
    assert len(periods) == count
    assert len(frame_counts) == count

    # TODO: network model change => include differentation between ES and SW?

    