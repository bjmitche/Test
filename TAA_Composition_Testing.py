
def test_calculation(taa_indices):
    balanced_index = taa_indices.index['Sterling Balanced']
    balanced_allocation = taa_indices.allocation_data.data_daily['Sterling Balanced']
    performance = taa_indices.index_data.performance_cum
    index = balanced_index*performance
    index = index*balanced_allocation
    index_sum = index.sum(axis=1)
    return index_sum
    
def test_2(taa_indices):
    pci_allocation = taa_indices.allocation_data.data_daily['Sterling Balanced']
    pci_index = taa_indices.index['Sterling Balanced']
    performance = taa_indices.index_data.performance_cum
    index = pci_index*performance
    index = index*pci_allocation
    index_sum = index.sum(axis=1)