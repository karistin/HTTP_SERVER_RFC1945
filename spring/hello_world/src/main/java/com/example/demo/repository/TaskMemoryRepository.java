package com.example.demo.repository;

import com.example.demo.domain.Task;

import java.util.*;

public class TaskMemoryRepository implements TaskRepository{

    private static Map<Long, Task> store = new HashMap<>();
    private static long sequence = 0L;


    @Override
    public Task save(Task task) {
        task.setTaskId(++sequence);
        store.put(task.getTaskId(), task);
        return null;
    }

    @Override
    public Optional<Task> findId(Long id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public List<Task> findAll() {
        return new ArrayList<>(store.values());
    }
}
