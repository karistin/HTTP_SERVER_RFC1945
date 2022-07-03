package com.example.demo.repository;

import com.example.demo.domain.Task;
import org.springframework.http.HttpStatus;

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

    public boolean deleteId(Long id){
        if (findId(id).isPresent())
        {
            store.remove(id);
            return true;
        }
        else{
            return false;
        }
    }

    public boolean amendTask(Long id, Task task){
        task.setTaskId(id);
        if (store.replace(id, task) == null)
        {
            return false;
        }
        return true;
    }
}
