package com.example.demo.controller;

import com.example.demo.domain.Task;
import com.example.demo.repository.TaskMemoryRepository;
import com.example.demo.repository.TaskRepository;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/tasks")
public class GreetingController {
    TaskRepository taskRepository = new TaskMemoryRepository();


    @GetMapping()
    @ResponseBody()
    public List<Task> GetApi(){
        return taskRepository.findAll();
    }

    @GetMapping("taskId")
    @ResponseBody()
    public Optional<Task> GetApi(@RequestParam("taskId") Long taskId){
        return taskRepository.findId(taskId);
    }

    @PostMapping()
    @ResponseBody()
    public Long PostApi(@RequestBody HashMap<String, String> map){
        Task task = new Task();
        task.setTitle(map.get("title"));
        task.setContents(map.get("contents"));
        taskRepository.save(task);
        return task.getTaskId();
    }

//    @PutMapping()
//    @ResponseStatus
//curl localhost:8888/tasks  -v -X POST -H Content-Type:application/json -d  "{"title": "string","contents":"123123"}"
//wsl python request not work???
}

