from datetime import datetime
from time import time
from typing import List, Type
import numpy as np
import math as math
import random as random


class Vector3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3'):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3'):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float):
        return Vector3(self.x * other, self.y * other, self.z * other)

    def getMagnitude(self) -> float:
        return math.sqrt((self.x*self.x) + (self.y*self.y) + (self.z*self.z))

    def toList(self) -> List:
        return [self.x, self.y, self.z]

    def normalized(self):
        mag = self.getMagnitude()
        if mag == 0:
            return Vector3(0,0,0)
        return Vector3(self.x/mag, self.y/mag, self.z/mag)

    @staticmethod
    def distance(vector_a: 'Vector3', vector_b: 'Vector3') -> float:
        return (vector_b - vector_a).getMagnitude()

    @staticmethod
    def listToVector3(list):
        return Vector3(list[0], list[1], list[2])


class Drone:
    def __init__(self, id:str, position: Vector3, target: 'Target' = None):
        self.id = id
        self.position: Vector3 = position
        self.target: Target = None


class Target:
    def __init__(self, position: Vector3):
        self.position: Vector3 = position
        self.target_drone: Drone = None


class FleetController:
    min_drone_separation: float = 3

    def __init__(self):
        self.all_drones: List[Drone] = []
        self.nextDroneId: int = 0

    def addNewDrone(self, x, y, z) -> Drone:
        drone: Drone = Drone(self.nextDroneId, Vector3(float(x), float(y), float(z)))
        self.nextDroneId += 1
        self.all_drones.append(drone)
        return drone

    def assignFirstMatchTaken(self, all_targets: List[Target]):
        drone: Drone
        for drone in self.all_drones:
            min_dist: float = float("inf")
            target: Target
            for target in all_targets:
                dist: float = Vector3.distance(drone.position, target.position)
                if dist < min_dist:
                    min_dist = dist
                    drone.target = target
            if drone.target is not None:
                drone.target.target_drone = drone

    def getAllDrones(self) -> List[Drone]:
        return self.all_drones

    def registerExistingDrone(self, id, x, y, z):
        print("Registered id: " + str(id))
        drone: Drone = Drone(id, Vector3(float(x),float(y),float(z)))
        self.all_drones.append(drone)

    @staticmethod
    def findLocNearPoint(target_point: Vector3, used_targets: List[Target]) -> Vector3:
        return_point: Vector3 = target_point
        used_tar: Target
        for used_tar in used_targets:
            if Vector3.distance(return_point, used_tar.position) < FleetController.min_drone_separation:
                avg_dir: Vector3 = Vector3(0, 0, 0)
                this_tar: Target
                for this_tar in used_targets:
                    avg_dir += (this_tar.position - return_point).normalized()
                avg_dir = avg_dir * (1/len(used_targets))
                avg_dir = avg_dir.normalized()
                avg_dir *= -1
                if avg_dir.getMagnitude() < Vector3(0.1, 0.1, 0.1).getMagnitude():
                    print("Choosing random direction")
                    random.seed(time)
                    avg_dir = Vector3(random.random()*2.0 - 1.0, random.random()*2.0 - 1.0, random.random()*2.0 - 1.0).normalized()
                return_point += avg_dir * FleetController.min_drone_separation
                return FleetController.findLocNearPoint(return_point, used_targets)
        return return_point

    def getDroneLocationsAboutPoint(self, point: Vector3) -> List[Target]:
        all_drones: List[Drone] = self.all_drones
        used_targets: List[Target] = []
        drone: Drone
        for drone in all_drones:
            new_pos = FleetController.findLocNearPoint(point, used_targets)
            tar = Target(new_pos)
            tar.targetDrone = drone
            used_targets.append(tar)

        return used_targets

    @staticmethod
    def getDroneLocationsCircle(self, radius: float, center_position: Vector3 = Vector3(0, 0, 0), up_dir: Vector3 = Vector3(0, 1, 0), normal_dir: Vector3 = Vector3(0, 0, 0)) -> List[Target]:
        cur_up_angle: Vector3 = up_dir
        all_drones: List[Drone] = self.getAllDrones()
        angle_delta: float = 2*math.pi/len(all_drones)
        cross_angle: Vector3 = Vector3.listToVector3((np.cross(cur_angle.toList(), normal_dir.toList())).tolist())
        return []
